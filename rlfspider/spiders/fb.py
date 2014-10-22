# -*- coding: utf-8 -*-

import re, codecs, json, urllib
from scrapy import Selector, Spider, log
from scrapy.http import Request, FormRequest
from rlfspider.items import ProfileItem, PageItem
from realfie.core.models import FbUser

REGEXES = {
    'bp_initial': re.compile('bigPipe.onPageletArrive\((\{.*"content":\{"initial_browse_result".*)\)'),
    'bp_browse': re.compile('bigPipe.onPageletArrive\((\{.*browse_result_below_fold":\{"container_id".*)\)'),
    'url_noparams': re.compile('\?.*'),
}

MAX_PAGES = 10

class FbSpider(Spider):
    name = "fb"
    allowed_domains = ["facebook.com"]
    start_urls = (
        'https://www.facebook.com/',
    )

    def __init__(self, task_entry, *args, **kwargs):
        self.task_entry = task_entry
        self.fbuser = FbUser.objects.filter(fbid=task_entry.uid).first()
        return super(FbSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = {
            'email':'turutanov@gmail.com',
            'pass':'fgh!!!34',
        }

        return [FormRequest.from_response(response, formname='login_form', formdata=data, callback=self.after_login)]

    def after_login(self, response):
        if "Timeline" not in response.body:
                self.log("Authentication failed!", level=log.ERROR)
                return

        fbid = self.fbuser.fbid
        gender = 'females' if self.fbuser.gender == 'male' else 'males'
        url = 'https://www.facebook.com/search/{0}/residents-near/intersect/{0}/pages-liked/likers/{0}/friends/friends/{1}/intersect'.format(fbid, gender)
        self.log("Query URL: {0}".format(url), level=log.INFO)

        return Request(url, dont_filter=True, callback=self.page_parse)

    def page_parse(self, response):
        data = response.meta.get('data')
        card_class = response.meta.get('card_class')
        liked_by = response.meta.get('liked_by')
        body = response.body

        if 'data' not in response.meta.keys():
            # parse the first page
            s = Selector(response)

            hidden_elems = s.xpath('//code[@class="hidden_elem"]/comment()').extract()
            # FIXME
            payload = ''.join([e[5:-4] for e in hidden_elems if 'sub_headers&quot;&#125;' in e])

            if not liked_by:
                # extract bigPipe parameters for subsequent requests
                initial_data = json.loads(REGEXES['bp_initial'].findall(body)[0])

                for r in initial_data['jsmods']['require']:
                    if r[0] == 'BrowseScrollingPager':
                        data = r[3][1]
                        break

                if not data:
                    self.log("Got no data for the next page!", level=log.ERROR)
                    #self.task_entry.status = 'failed'
                    #self.task_entry.save()
                    return

                #self.log("Page request data: {0}".format(data), level=log.INFO)

                # contains cursor to the next page
                try:
                    requires = json.loads(REGEXES['bp_browse'].findall(body)[0])['jsmods']['require']
                except IndexError:
                    self.log("Cursor not found on the first page!", level=log.ERROR)
                    self.task_entry.status = 'failed'
                    self.task_entry.save()
                    return

        else:
            # subsequent pages
            browse_data = json.loads(body[9:])
            payload = browse_data['payload']

            # contains cursor to the next page
            requires = browse_data['jsmods']['require']

        page_number = 1

        if not liked_by:
            page_number = data.get('page_number', 1)
            filename = '{0}.html'.format(page_number)
        else:
            filename = '{0}_likes.html'.format(liked_by)            

        with codecs.open(filename, 'wb', 'utf-8') as f:
            f.write(payload)

        s = Selector(text=payload)

        # get profile card container CSS class name
        if not card_class:
            card_class = s.xpath("//div[@id='BrowseResultsContainer']/div/@class")[0].extract()

        # profile cards are selected by this class
        profile_elems = s.xpath("//div[starts-with(@class, '{0}')]".format(card_class))

        if not liked_by:
            # extract basic info
            for e in profile_elems:
                lid = json.loads(e.xpath(".//div[starts-with(@data-bt, '{\"id\"')]/@data-bt")[0].extract())['id']
                link = e.xpath(".//div[@data-bt='{\"ct\":\"title\"}']/a/@href")[0].extract()
                link = REGEXES['url_noparams'].sub('', link)
                
                yield ProfileItem(
                    id=lid,
                    name=e.xpath(".//div[@data-bt='{\"ct\":\"title\"}']/a/text()")[0].extract(),
                    photo=e.xpath(".//a[@data-bt='{\"ct\":\"image\"}']/img/@src")[0].extract(),
                    link=link
                )

                url = 'https://www.facebook.com/search/{0}/pages-liked/{1}/pages-liked/intersect?ref=snippets'.format(self.fbuser.fbid, lid)
                request = Request(url, dont_filter=True, callback=self.page_parse)
                request.meta['liked_by'] = lid
                yield request
        else:
            for e in profile_elems:
                lid = json.loads(e.xpath(".//div[starts-with(@data-bt, '{\"id\"')]/@data-bt")[0].extract())['id']
                link = e.xpath(".//div[@data-bt='{\"ct\":\"title\"}']/a/@href")[0].extract()
                link = REGEXES['url_noparams'].sub('', link)
                
                yield PageItem(
                    id=lid,
                    name=e.xpath(".//div[@data-bt='{\"ct\":\"title\"}']/a/text()")[0].extract(),
                    type=e.xpath(".//div[@data-bt='{\"ct\":\"sub_headers\"}']/text()")[0].extract(),
                    photo=e.xpath(".//a[@data-bt='{\"ct\":\"image\"}']/img/@src")[0].extract(),
                    link=link,
                    liked_by=response.meta['liked_by']
                )            

        if page_number >= MAX_PAGES or liked_by:
            return

        # is last page?
        eor = s.xpath('//div[@id="browse_end_of_results_footer"]')
        if len(eor):
            return

        # get cursor for the next page
        for r in requires:
            if r[0] == 'BrowseScrollingPager':
                data.update(r[3][0])
                break

        self.log("Page request data: {0}".format(data), level=log.INFO)

        # prepare for next page
        url = '{0}?data={1}&__a=1'.format(
            'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet',
            urllib.quote(json.dumps(data, separators=(',', ':')))
        )
        request = Request(url, dont_filter=True, callback=self.page_parse)
        request.meta['data'] = data
        request.meta['card_class'] = card_class
        
        yield request

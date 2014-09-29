# -*- coding: utf-8 -*-

import re, codecs, json, urllib
from scrapy import Selector, Spider, log
from scrapy.http import Request, FormRequest
from rlfspider.items import ProfileItem

REGEXES = {
    'bp_initial': re.compile('bigPipe.onPageletArrive\((\{.*"content":\{"initial_browse_result".*)\)'),
    'bp_browse': re.compile('bigPipe.onPageletArrive\((\{.*browse_result_below_fold":\{"container_id".*)\)'),
}

MAX_PAGES = 3

class FbSpider(Spider):
    name = "fb"
    allowed_domains = ["facebook.com"]
    start_urls = (
        'https://www.facebook.com/',
    )

    def __init__(self, rlf_user, *args, **kwargs):
        self.rlf_user = rlf_user
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

        url = 'https://www.facebook.com/search/{0}/pages-liked/likers/{0}/friends/friends/intersect'.format(self.rlf_user.fbid)
        self.log("Query URL: {0}".format(url), level=log.INFO)
        #'https://www.facebook.com/search/me/friends',

        return Request(url, dont_filter=True, callback=self.page_parse)

    def page_parse(self, response):
        data = response.meta.get('data')
        profile_class = response.meta.get('profile_class')
        body = response.body

        if 'data' not in response.meta.keys():
            # parse the first page
            s = Selector(response)

            hidden_elems = s.xpath('//code[@class="hidden_elem"]/comment()').extract()
            # FIXME
            payload = ''.join([e[5:-4] for e in hidden_elems if 'sub_headers&quot;&#125;' in e])

            # extract bigPipe parameters for subsequent requests
            initial_data = json.loads(REGEXES['bp_initial'].findall(body)[0])

            for r in initial_data['jsmods']['require']:
                if r[0] == 'BrowseScrollingPager':
                    data = r[3][1]
                    break

            if not data:
                self.log("Got no data for the next page!", level=log.ERROR)
                return

            self.log("Page request data: {0}".format(data), level=log.INFO)

            # contains cursor to the next page
            try:
                requires = json.loads(REGEXES['bp_browse'].findall(body)[0])['jsmods']['require']
            except IndexError:
                self.log("Cursor not found on the first page!", level=log.ERROR)
                return

        else:
            # subsequent pages
            browse_data = json.loads(body[9:])
            payload = browse_data['payload']

            # contains cursor to the next page
            requires = browse_data['jsmods']['require']

        page_number = data.get('page_number', 1)

        """
        with codecs.open('{0}.html'.format(page_number), 'wb', 'utf-8') as f:
            f.write(payload)
        """

        s = Selector(text=payload)

        # get profile card container CSS class name
        if not profile_class:
            profile_class = s.xpath("//div[@id='BrowseResultsContainer']/div/@class")[0].extract()

        # profile cards are selected by this class
        profile_elems = s.xpath("//div[starts-with(@class, '{0}')]".format(profile_class))

        # extract basic info
        for e in profile_elems:
            yield ProfileItem(
                id=json.loads(e.xpath(".//div[starts-with(@data-bt, '{\"id\"')]/@data-bt")[0].extract())['id'],
                name=e.xpath(".//div[@data-bt='{\"ct\":\"title\"}']/a/text()")[0].extract(),
                photo=e.xpath(".//a[@data-bt='{\"ct\":\"image\"}']/img/@src")[0].extract()
            )

        if page_number >= MAX_PAGES:
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

        # prepare for next page
        url = '{0}?data={1}&__a=1'.format(
            'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet',
            urllib.quote(json.dumps(data, separators=(',', ':')))
        )
        request = Request(url, dont_filter=True, callback=self.page_parse)
        request.meta['data'] = data
        request.meta['profile_class'] = profile_class
        
        yield request

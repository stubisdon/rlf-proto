import os, urllib2, json, math
from billiard import Process
from twisted.internet import reactor
from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from rlfspider.spiders.fb import FbSpider
from realfie.core.models import IgUser

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'rlfspider.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realfie.settings.default')

class CrawlerProcess(Process):
        def __init__(self, rlf_user):
            Process.__init__(self)
            
            crawler = Crawler(get_project_settings())
            crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            crawler.configure()
            
            self.crawler = crawler
            self.spider = FbSpider(rlf_user)

        def run(self):
            settings = self.crawler.settings
            self.crawler.crawl(self.spider)
            self.crawler.start()
            log.start(logfile=settings['LOG_FILE'], loglevel=settings['LOG_LEVEL'], logstdout=settings['LOG_STDOUT'])
            reactor.run()

def run_spider(task):
    crawler = CrawlerProcess(task)
    crawler.start()
    crawler.join()

def run_ig(task, token):
        data_self = ig_get('users/self', token)

        task.uid = data_self['id']
        task.save()

        data_feed = ig_get('users/self/media/recent', token)            
        
        tag_count = {}
        tag_locations = {}

        for entry in data_feed:
            tags = entry['tags']
            location = entry['location']

            if tags and location:
                for tag in tags:
                    try:
                        tag_count[tag] += 1
                    except KeyError:
                        tag_count[tag] = 1
                    
                    """
                    loc = {
                        'latitude': round(location['latitude'] * 5) / 5,
                        'longitude': round(location['longitude'] * 5) / 5
                    }
                    """
                    loc = location

                    if not (tag in tag_locations and loc in tag_locations[tag]):
                        try:
                            tag_locations[tag].append(loc)
                        except KeyError:
                            tag_locations[tag] = [loc]

        sorted_tags = sorted(tag_count, key=tag_count.get, reverse=True)

        print 'tc', tag_count
        print 'tl', tag_locations
        print 'st', sorted_tags

        if not sorted_tags:
            task.status = 'failed'
            task.save()
            return

        matches = {}
        lookup_tags = sorted_tags if len(sorted_tags) <= 5 else sorted_tags[:5]

        for tag in lookup_tags:
            recent_for_tag = ig_get('tags/{0}/media/recent'.format(sorted_tags[0]), token)
           
            radius_expand = [10, 20, 50, 100, 200, 500, 1000, 5000, 10000]
            for radius in radius_expand:
                radius_matches = {}

                for entry in recent_for_tag:
                    loc = entry['location']

                    if not loc:
                        continue

                    lat_dt = radius / 111.1
                    lng_dt = radius / 111.32 * math.cos(loc['latitude'] / 180 * math.pi)
                    #print 'dt', lat_dt, lng_dt

                    for tag_loc in tag_locations[sorted_tags[0]]:
                        #print 'cmp dt', abs(loc['latitude'] - tag_loc['latitude']), abs(loc['longitude'] - tag_loc['longitude'])
                        if abs(loc['latitude'] - tag_loc['latitude']) <= lat_dt and abs(loc['longitude'] - tag_loc['longitude']) <= lng_dt:
                            radius_matches[entry['user']['username']] = entry['user']

                try:
                    matches[radius] += radius_matches.values()
                except KeyError:
                    matches[radius] = radius_matches.values()

        print matches
        m = None
        for k in radius_expand:
            if not k in matches:
                break
            if not len(matches[k]):
                continue

            m = matches[k][0]
            break

        if not m:
            task.status = 'failed'
            task.save()
            return

        # GARBAGE
        """
        likers = {}

        for entry in data_feed:
            likes = entry['likes']
            if not likes['count']:
                continue

            for l in likes['data']:
                inid = l['id']

                try:
                    likers[inid] += 1
                except KeyError:
                    likers[inid] = 1

        if not len(likers):
            return JsonResponse({
                'task_id': 0,
                'status': 'failed',
                'progress': 0,
                'entries': [],
            })  

        likers_s = sorted(likers, key=likers.get, reverse=True)

        data_liker = ig_get('users/{0}'.format(likers_s[0]), token)
        """

        iguser = IgUser(
            igid=m['id'],
            name=m['full_name'] or m['username'],
            photo=m['profile_picture'],
            task=task

        )

        iguser.save()
        task.status = 'completed'
        task.save()


def ig_get(endpoint, access_token):
    url = 'https://api.instagram.com/v1/{0}?access_token={1}'.format(endpoint, access_token)
    request = urllib2.Request(url)
    data = json.loads(urllib2.urlopen(request).read())
    
    if data['meta']['code'] == 200:
        return data['data']
    
    return None

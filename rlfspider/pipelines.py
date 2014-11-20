from __future__ import division
from datetime import datetime
from realfie.core.models import FbUser, FbPage
from items import ProfileItem, PageItem


class RlfspiderPipeline(object):
    users = {}
    pages = []
    fbuser = None

    def open_spider(self, spider):
        self.task = spider.task_entry
        self.task.status = 'ongoing'
        self.task.save()

    def process_item(self, item, spider):
        if isinstance(item, ProfileItem):
            user = FbUser.objects.filter(fbid=item['id']).first()

            if not user:
                user = FbUser(fbid=item['id'])

            user.name = item['name']
            user.photo = item['photo']
            user.link = item['link']
            user.gender = item['gender']
            user.task = self.task
    
            user.save()
    
            self.users[user.fbid] = user

            self.task.progress = len(self.users) / (spider.CARDS_PER_PAGE * spider.MAX_PAGES)
            self.task.save()
        
        else:
            page = FbPage.objects.filter(page_id=item['id']).first()

            if not page:
                page = FbPage(page_id=item['id'])

            page.name = item['name']
            page.type = item['type']
            page.photo = item['photo']
            page.link = item['link']

            page.save()

            if not self.fbuser:
                self.fbuser = FbUser.objects.get(fbid=self.task.uid)

            page.liked_by.add(self.fbuser, self.users[item['liked_by']])
    
            self.pages.append(page)

        return item

    def close_spider(self, spider):
        # Oh boy this is going to be slow
        # Can't bulk create anymore because of m2m
        #FbUser.objects.bulk_create(self.users)
        
        if self.task.status == 'ongoing':
            self.task.status = 'completed'
            self.task.message = "Fetched {0} users and {1} pages.".format(len(self.users.keys()), len(self.pages))

        self.task.finished = datetime.now()
        self.task.save()

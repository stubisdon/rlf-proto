from realfie.core.models import FbUser
from datetime import datetime

class RlfspiderPipeline(object):
    items = []

    def open_spider(self, spider):
        self.rlf_user = spider.rlf_user
        self.rlf_user.status = 'P'
        self.rlf_user.save()

    def process_item(self, item, spider):
        user = FbUser(
            fbid=item['id'],
            name=item['name'],
            photo=item['photo'],
            task=self.rlf_user
        )
        
        self.items.append(user)
        return item

    def close_spider(self, spider):
        FbUser.objects.bulk_create(self.items)
        self.rlf_user.finished = datetime.now()
        self.rlf_user.status = 'OK'
        self.rlf_user.save()

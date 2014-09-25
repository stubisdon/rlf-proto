from realfie.core.models import FbUser


class RlfspiderPipeline(object):
    items = []

    def open_spider(self, spider):
        self.rlf_user = spider.rlf_user

    def process_item(self, item, spider):
        user = FbUser(
            fbid=item['id'],
            name=item['name'],
            photo=item['photo'],
            friend_of=self.rlf_user
        )
        
        self.items.append(user)
        return item

    def close_spider(self, spider):
        FbUser.objects.bulk_create(self.items)

import src.static as static
import time
from src.helpers import get_absolute_links, to_sha1


class LinkVisitor:
    def __int__(self, homepages, topic):
        self.homepages = homepages
        self.topic = topic

    def visit_one(self):
        for homepage in self.homepages:
            # send encoded home page to redis anh add to kafka consumer
            all_urls = get_absolute_links(homepage)
            for url in all_urls:
                encoded_url = to_sha1(url)
                if not static.redis.exists(encoded_url):
                    # add new url to redis and add original to kafka producer
                    static.redis.set(encoded_url, None)
                    static.producer.send(self.topic, url)

    def visit(self):
        while True:
            # visit available homepages every 60s
            self.visit_one()
            time.sleep(60)

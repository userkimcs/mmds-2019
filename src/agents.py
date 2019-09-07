import src.static as static
import time
from src.helpers import *
from newspaper import Article


def add_articles(kk_host, kk_port, kk_url_topic=static.Topic.articles):
    article_consumer = static.create_consumer(kk_host, kk_port, kk_url_topic)
    for article in article_consumer:
        article = article.value
        static.mongodb['document'].insert_one(article)


def get_articles(kk_host, kk_port, kk_link_topic=static.Topic.newlinks, kk_url_topic=static.Topic.articles):
    """

    :param kk_host:
    :param kk_port:
    :param kk_link_topic:
    :param kk_url_topic:
    :return:
    """
    link_consumer = static.create_consumer(kk_host, kk_port, kk_link_topic)
    article_producer = static.create_producer(kk_host, kk_port)

    for message in link_consumer:
        message = message.value
        url = message['url']
        article = Article(url)
        article.download()
        # add article object (full text, title, date, authors)
        article_dict = dict()
        article_dict['url'] = url
        article_dict['text'] = article.text
        article_dict['title'] = article.title
        article_dict['authors'] = article.authors
        article_dict['date'] = article.publish_date
        article_producer.send(kk_url_topic, article_dict)


def visit(homepages, kk_host, kk_port, kk_topic=static.Topic.links, sleep=60):
    """

    :param homepages:
    :param kk_host:
    :param kk_port:
    :param kk_topic:
    :param sleep:
    :return:
    """

    producer = static.create_producer(kk_host, kk_port)
    while True:
        time.sleep(sleep)
        for homepage in homepages:
            # send encoded home page to redis anh add to kafka consumer
            all_urls = get_absolute_links(homepage)
            for url in all_urls:
                url = normalize_url(url)
                encoded_url = to_sha1(url)
                if not static.redis.exists(encoded_url):
                    # add new url to redis and add original to kafka producer
                    static.redis.set(encoded_url, None)
                    producer.send(kk_topic, value={'url': url})

import json
import kafka
import argparse
from newspaper import Article
import pymongo


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka_host", required=False, default='127.0.0.1')
    parser.add_argument("--kafka_port", required=False, type=int, default=9092)
    parser.add_argument("--kafka_topic", required=False, default='default')
    parser.add_argument("--mongodb_host", required=False, default='127.0.0.1')
    parser.add_argument("--mongodb_port", required=False, type=int, default=27017)
    parser.add_argument("--mongodb", required=False, default='default')
    parser.add_argument("--mongodb_collection", required=False, default='document')

    args = parser.parse_args()

    consumer = kafka.KafkaConsumer(bootstrap_servers='{}:{}'.format(args.kafka_host, args.kafka_port))

    consumer.subscribe([args.kafka_topic])

    mongo_client = pymongo.MongoClient(host=args.mongodb_host, port=args.mongodb_port)

    mongodb = mongo_client[args.mongodb]

    for message in consumer:
        url = message.value.decode()

        article = Article(url)
        article.download()
        # add article object (full text, title, date, authors)
        article_dict = dict()
        article_dict['url'] = url
        article_dict['text'] = article.text
        article_dict['title'] = article.title
        article_dict['authors'] = article.authors
        article_dict['date'] = article.publish_date

        # insert
        mongodb[args.mongodb_collection].insert_one(article_dict)


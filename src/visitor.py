import json
import kafka
import argparse
import time
import redis

from src.helpers import get_absolute_links, normalize_url, to_sha1

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka_host", required=False, default='127.0.0.1')
    parser.add_argument("--kafka_port", required=False, type=int, default=9092)
    parser.add_argument("--kafka_topic", required=False, default='default')
    parser.add_argument("--homepages", required=True)
    parser.add_argument("--redis_host", required=False, default='127.0.0.1')
    parser.add_argument("--redis_port", required=False, type=int, default=6379)
    parser.add_argument("--sleep", required=False, type=int, default=10)

    args = parser.parse_args()

    producer = kafka.KafkaProducer(bootstrap_servers="{}:{}".format(args.kafka_host, args.kafka_port))

    exist_urls = redis.Redis(host=args.redis_host, port=args.redis_port)

    # load homepages
    homepages = open(args.homepages).readlines()

    while True:

        for homepage in homepages:
            homepage = homepage.strip()
            # send encoded home page to redis anh add to kafka consumer
            all_urls = get_absolute_links(homepage)
            for url in all_urls:
                url = normalize_url(url)
                encoded_url = to_sha1(url)
                if not exist_urls.exists(encoded_url):
                    # add new url to redis and add original to kafka producer
                    exist_urls.set(encoded_url, 0)
                    producer.send(args.kafka_topic, url.encode())

        time.sleep(args.sleep)

import json

import redis
from kafka import KafkaProducer, KafkaConsumer
from pymongo import MongoClient

redis = redis.Redis()
_mongo_client = MongoClient()
mongodb = _mongo_client['default']


def create_producer(host, port):
    return KafkaProducer(bootstrap_servers="{}:{}".format(host, port),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def create_consumer(host, port, topic):
    return KafkaConsumer(topic,
                         bootstrap_servers="{}:{}".format(host, port),
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


class Topic:
    default = 'default'
    links = 'links'
    newlinks = 'newlinks'
    articles = 'articles'

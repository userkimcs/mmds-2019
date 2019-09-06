import redis
import kafka


redis = redis.Redis()

producer = kafka.KafkaProducer()

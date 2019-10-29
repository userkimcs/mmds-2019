import kafka
from newspaper import Article
from arguments import configs
from helpers import DatabaseService, DatabaseModel, get_keywords, insert_pipeline
import nltk


def download_nltk():
    nltk.download('words')
    nltk.download('maxent_ne_chunker')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')


if __name__ == "__main__":

    download_nltk()

    consumer = kafka.KafkaConsumer(configs.kafka_link_topic,
                                   bootstrap_servers=configs.kafka_host,
                                   group_id=configs.kafka_default_group)

    stream_producer = kafka.KafkaProducer(bootstrap_servers=configs.kafka_host)

    # connect pg
    pg = DatabaseService(host=configs.pg_host, user=configs.pg_user,
                         password=configs.pg_password, port=configs.pg_port,
                         database=configs.pg_db)

    for message in consumer:
        url = message.value.decode("utf-8")

        article = Article(url)
        article.download()
        # add article object (full text, title, date, authors)
        article_dict = dict()
        article_dict['url'] = url
        article_dict['text'] = article.text
        article_dict['title'] = article.title
        article_dict['authors'] = article.authors
        article_dict['date'] = article.publish_date

        keywords = get_keywords(article.text)
        keywords.extend(get_keywords(article.title))

        model = DatabaseModel()
        model.data = article_dict
        # insert
        pg.insert_one(model)

        # send to kk
        insert_pipeline(stream_producer, keywords)



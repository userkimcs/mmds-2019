import argparse
import sys


def create_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--kafka_host", required=True, help="Kafka host. Example: 127.0.0.1:9092")
    parser.add_argument("--kafka_link_topic", required=False, help="Kafka link topic")
    parser.add_argument("--kafka_keyword_topic", required=False, default="keywords",
                        help="""Kafka keyword topic. Use this option if you need to stream into pipelinedb""")

    parser.add_argument("--kafka_default_group", required=False, help="Default consumer group", default="default")

    parser.add_argument("--redis_host", required=True, help="Redis server")
    parser.add_argument("--redis_port", required=False, help="Redis port", default=6379)
    parser.add_argument("--redis_db", required=False, help="Redis database number", default=1)
    parser.add_argument("--redis_password", required=False, help="Redis authentication password", default=None)

    parser.add_argument("--pg_host", required=True)
    parser.add_argument("--pg_port", required=False, default=5432)
    parser.add_argument("--pg_user", required=True)
    parser.add_argument("--pg_password", required=True)
    parser.add_argument("--pg_db", required=False, default="data")
    parser.add_argument("--pg_relation", required=True)

    cfg = parser.parse_args(args)
    return cfg


configs = create_arguments()

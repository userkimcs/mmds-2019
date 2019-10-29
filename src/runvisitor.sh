#!/bin/bash

export PYTHONPATH=/src
python3 visitor.py \
--kafka_host=127.0.0.1 \
--redis_host=127.0.0.1 \
--pg_host=10.10.0.12 \
--pg_user=myuser \
--pg_password=123456 \
--pg_relation=data
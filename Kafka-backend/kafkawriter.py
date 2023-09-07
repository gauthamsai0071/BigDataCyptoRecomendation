from pykafka import KafkaClient
import threading

def init_kafkawriter():

    KAFKA_HOST = "localhost:9092" # Or the address you want

    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics["solusdt"]

def log_kafka(symbol, message):
    KAFKA_HOST = "localhost:9092"
    client = KafkaClient(hosts = KAFKA_HOST)
    topic = client.topics[symbol]
    with topic.get_sync_producer() as producer:
        encoded_message = message.encode("utf-8")
        producer.produce(encoded_message)

def log_kafka_trade(symbol, message):
    KAFKA_HOST = "localhost:9092"
    client = KafkaClient(hosts = KAFKA_HOST)
    trade_symbol = "trade"+symbol
    topic = client.topics[trade_symbol]
    with topic.get_sync_producer() as producer:
        encoded_message = message.encode("utf-8")
        producer.produce(encoded_message)
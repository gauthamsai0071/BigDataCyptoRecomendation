from kafka import KafkaConsumer
import sys
from json import loads

def read_kafka(topic, group):
    KAFKA_HOST = "localhost:9092" # Or the address you want
    consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[KAFKA_HOST],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=group,
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000)
    messages = []
    for message in consumer:
        consumer.commit()
        # print(message.value)
        messages.append(message.value)
    
    consumer.close()
    return messages

def read_kafka_trade(topic, group):
    KAFKA_HOST = "localhost:9092" # Or the address you want
    trade_topic = "trade"+topic
    consumer = KafkaConsumer(
    trade_topic,
    bootstrap_servers=[KAFKA_HOST],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=group,
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000)
    messages = []
    for message in consumer:
        consumer.commit()
        # print(message.value)
        messages.append(message.value)
    
    consumer.close()
    return messages


if __name__ == "__main__":
    topic = sys.argv[1]
    group = sys.argv[2]
    print("topic: " + topic)
    read_kafka(topic, group)


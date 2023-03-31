from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

class KafkaBuffer:
    def __init__(self, config):
        self.config = config
        self.admin = AdminClient(config)
        self.producer = Producer(config)
        self.consumer = Consumer(config)

    def create_topic(self, topic_name):
        topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        self.admin.create_topics([topic])

    def produce(self, topic_name, message):
        self.producer.produce(topic_name, message)
        self.producer.flush()

    def consume(self, topic_name):
        self.consumer.subscribe([topic_name])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            yield msg.value().decode('utf-8')
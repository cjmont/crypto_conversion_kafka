import datetime
import logging
from datetime import datetime
from typing import List

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import TopicPartition
from notbank.base.models.base import Log
from notbank.tasks.trama_consumer import TramaConsumer


class Consumer:
    logger: logging.Logger
    consumer: KafkaConsumer
    running: bool

    def __init__(self, topics: List[str], group_id: str, servers: List[str]):
        self.logger = logging.getLogger('kafka_consumer.'+__name__)
        # keep it in debug, effective logger level is setted in the config file
        self.logger.setLevel(logging.DEBUG)
        self.consumer = KafkaConsumer({
            'bootstrap.servers': ','.join(servers),
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': 'false',
            'max.poll.interval.ms': 60000,
            'session.timeout.ms': 30000
        })
        self.running = False
        self.consumer.subscribe(topics)

    def safe_stop(self, signum, frame):
        self.logger.info(f'stop signal {signum} recieved, making a safe stop')
        self.running = False

    def start(self):
        self.running = True
        try:
            self.logger.debug('starting reading loop')
            while self.running:
                messages = self.consumer.consume(10, 0.1)
                for message in messages:
                    self.consume_message(message)
            self.logger.debug('reading loop stopped')
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.consumer.close()
            self.logger.debug('kafka consumer closed')

    def consume_message(self, message):
        if message is None:
            # No message available within timeout.
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            self.logger.debug(
                "Waiting for message or event/error in consume()"
            )
            return
        if message.error():
            self.logger.warn(message.error())
            Log.warning(
                message.error(),
                service=Log.SERVICE.KAFKA_CONSUMER
            )
            return

        # init_time = datetime.now()
        record_key = message.key()
        record_value = message.value()
        record_offset = message.offset()
        record_partition = message.partition()
        record_topic = message.topic()

        self.logger.info(''.join([
            f"[{record_topic}:{record_partition}:{record_offset}]",
            f"[{datetime.now()}] key={record_key} value={record_value}"
        ]))

        try:
            trama = record_value.decode('utf-8')
            TramaConsumer.consume_trama(trama, record_topic)
        except UnicodeError:
            error_msg = f'failed to decode, bytes of trama corrupted {record_topic}, ignoring message'
            Log.error(error_msg, Log.SERVICE.KAFKA_CONSUMER)

        partition = TopicPartition(
            topic=record_topic,
            partition=record_partition,
            offset=record_offset + 1,
        )
        self.consumer.commit(
            offsets=[partition],
            asynchronous=False,
        )

from confluent_kafka import Producer as KafkaProducer, KafkaException, KafkaError
from django.conf import settings

from notbank.base.models.base import Log


class Producer:
    @staticmethod
    def _send_kafka_message(servers: list, topic: str, message: str, sync: bool = True) -> bool:
        try:
            kafka_producer = KafkaProducer({
                'bootstrap.servers': ','.join(servers),
                'enable.idempotence': True
            })

            def acked(err, msg):
                if err is not None:
                    Log.error(
                        f'Failed to deliver message: {msg}: {err}',
                        Log.SERVICE.KAFKA_PRODUCER
                    )
                else:
                    print(f'Message produced: {msg}')
            kafka_producer.produce(
                topic=topic,
                key="some",
                value=bytes(message, 'utf-8'),
                callback=acked
            )
            if sync:
                # Wait for any outstanding messages to be delivered and delivery report
                # callbacks to be triggered.
                kafka_producer.flush()

            return True
        except BufferError:
            # if the internal producer message queue is full
            return False
        except KafkaException as exception:
            error: KafkaError = exception.args[0]
            Log.error(error.reason, Log.SERVICE.KAFKA_PRODUCER)
            return False
        except NotImplementedError:
            # if timestamp is specified without underlying library support.
            return False

    @staticmethod
    def send_kafka_message(topic: str, message: str, sync: bool = True) -> bool:
        return Producer._send_kafka_message(
            servers=settings.KAFKA_NOTBANK_SERVERS,
            topic=topic,
            message=message,
            sync=sync
        )

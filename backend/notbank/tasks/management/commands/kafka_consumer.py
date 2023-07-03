from email.policy import default
import signal

from django.core.management import BaseCommand
from django.conf import settings

from notbank.tasks.consumer import Consumer


class Command(BaseCommand):
    default_topic_list = [
        settings.KAFKA_NOTBANK_SYNC_TOPIC,
        settings.KAFKA_USER_DATA_TOPIC,
        settings.KAFKA_BALANCE_MANAGER_STATUS_TOPIC,
        settings.KAFKA_QUOTE_SERVICE_RESULT_TOPIC,
        settings.KAFKA_QUOTE_LISTENER_TOPIC,
        settings.KAFKA_NOTIFY_TRANSACTION_TOPIC,
        settings.KAFKA_RETURN_FEE_TOPIC,
        settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC
    ]
    help = f"Run kafka consumer. Default topic list to consume: {default_topic_list}"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '-t', '--topics',
            nargs='*',
            help='list of topics to consume. If not provided, consumes the default topic list'
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        group_id = settings.KAFKA_CELERY_GROUP
        servers = settings.KAFKA_NOTBANK_SERVERS
        topics = self.default_topic_list
        if options['topics']:
            topics = options['topics']
        print(topics)
        consumer = Consumer(topics=topics, group_id=group_id, servers=servers)
        # sigint = control-c, interactive atention signal
        signal.signal(signal.SIGINT, consumer.safe_stop)
        # sigterm = termination request
        signal.signal(signal.SIGTERM, consumer.safe_stop)

        consumer.start()

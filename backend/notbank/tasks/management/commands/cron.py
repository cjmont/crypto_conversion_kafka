from datetime import datetime

from django.core.management import BaseCommand
from django.conf import settings
from notbank.tasks.tasks import delete_quotes_until

from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        hourconfig = settings.DATE
        d = datetime.today() - hourconfig
        str_date = d.strftime("%Y-%m-%d %H:%M:%S")

        delete_quotes_until.delay(str_date)

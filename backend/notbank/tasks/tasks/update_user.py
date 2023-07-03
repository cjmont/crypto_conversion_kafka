
from celery import shared_task

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.user_data import UserData
from notbank.base.utils.time import datetime_from_timestamp
from notbank.tasks.tasks.shared import log_error_with_traceback
from notbank.transactions.models import User


@shared_task
def update_user(trama: str):
    try:
        user_data = UserData.from_trama(trama)
    except TramaFormatException:
        log_error_with_traceback(f'failed to parse trama:{trama}')
        return
    user, _ = User.objects.get_or_create(
        uuid=user_data.uuid,
        defaults={'created_at': datetime_from_timestamp(user_data.timestamp)},
    )
    if user_data.phone != '':
        user.phone = user_data.phone
    if user_data.firebase_token != '':
        user.firebase_token = user_data.firebase_token
    user.save()

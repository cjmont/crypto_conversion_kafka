from celery import shared_task

from notbank.base.utils.kafka.tramas.quote_service_internal_execute_out import QuoteServiceInternalExecuteOut
from notbank.tasks.tasks.shared import log_error_with_traceback
from notbank.transactions.models import Conversion, CurrentConversion


@shared_task
def update_conversion_status_quote_service(trama: str):
    data = QuoteServiceInternalExecuteOut.from_trama(trama)
    conversion = Conversion.objects.get(task_id=data.request_id)
    if conversion.status != Conversion.STATUS.BM_SUCCESS_QS_PENDING:
        log_error_with_traceback(
            f'conversion not waiting quote service. conversion (task_id={conversion.task_id}) with status={Conversion.STATUS(conversion.status).name} ')
    status_mapping = {
        QuoteServiceInternalExecuteOut.STATE.NOT_ENOUGH_BALANCE: Conversion.STATUS.QS_ERROR_NOT_ENOUGH_BALANCE,
        QuoteServiceInternalExecuteOut.STATE.NOT_POSSIBLE_TO_COMPLY: Conversion.STATUS.QS_ERROR_NOT_POSSIBLE_TO_COMPLY,
        QuoteServiceInternalExecuteOut.STATE.EXECUTED: Conversion.STATUS.QS_SUCCESS,
    }
    conversion.status = status_mapping[data.state]
    conversion.save()
    try:
        current = CurrentConversion.objects.get(request_id=conversion.task_id)
        # ! here lies logic particular to one instance, instead of all instances of the service
        current.delete()
    except CurrentConversion.DoesNotExist:
        pass

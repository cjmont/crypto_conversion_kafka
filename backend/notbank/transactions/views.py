
from crypt import methods
from email.header import Header
from inspect import Parameter
import traceback
import uuid
import jwt
from notbank.base.exceptions import InvalidArgumentException, NotBankAPIException, QuoteNotFoundException
import notbank.transactions.services as transfer_services
from django.conf import settings
from django.http import HttpRequest
from notbank.base.models.base import Log
from notbank.transactions.models import User
from notbank.transactions.serializers import TransferRequestSerializer, TransferSerializer, UserSerializer, CurrentConversionSerializer, QuoteSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


def error_response(exception: Exception = None) -> Response:
    response_dict = {
        'code': 500,
        'status': 'error',
        'message': 'Internal error'
    }
    if isinstance(exception, NotBankAPIException):
        response_dict = exception.to_dict()
    return Response(
        response_dict,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def is_valid_uuid(value: str):
    try:
        uuid.uuid(value)
        return True
    except ValueError:
        return False


def success_response(data: dict = {}) -> Response:
    return Response(
        {"status": "success", "data": data},
        status=status.HTTP_200_OK
    )


def authenticate_jwt(request: HttpRequest):

    try:
        key = settings.SIMPLE_JWT['SIGNING_KEY']
        authorization = request.headers.get('Authorization')
        if authorization and authorization.startswith('Bearer '):
            access_token = jwt.decode(
                authorization[7:], key, algorithms="HS256")
            # !Cambiar este valor por el uuid del usuario actualmente por propositos de prueba lo extraemos del issuer
            uuid = access_token['iss']

        return uuid
    except Exception as e:
        return None


class AuthenticatedAPIView(APIView):
    permission_classes = (IsAuthenticated,)


# get all transfer requests
class TransferRequestAll(AuthenticatedAPIView):
    def get(self, request: HttpRequest):
        page_size = 1
        try:
            estado = request.data['status']
            creacion = request.data['creation_date']
            transfer_request_list = transfer_services.get_transfer_request_list_all(
                status=estado, creation_date=creacion)
            serializer = TransferRequestSerializer(
                transfer_request_list,
                many=True
            )
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(
                transfer_request_list, request)
            serializer = TransferRequestSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)

# get the transfers request of a particular user


class TransferRequestView(AuthenticatedAPIView):

    def get(self, request: HttpRequest):
        try:
            user_uuid = request.data['user_uuid']  # TODO:  take it from jwt
            transfer_request_list = transfer_services.get_transfer_request_list_of_user(
                user_uuid=user_uuid
            )
            serializer = TransferSerializer(
                transfer_request_list,
                many=True
            )
            return success_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)

    def post(self, request: HttpRequest):
        try:
            transfer_services.sync_new_transfer_request(
                # TODO: get from_user_uuid from jwt
                # from_user_uuid=from_uuid,
                from_user_uuid=request.data['from_user_uuid'],
                # to_user_uuid=to_uuid,
                to_user_uuid=request.data['to_user_uuid'],
                currency=request.data['asset'],
                amount=request.data['amount'],
                fee_amount=request.data['fee_amount'],
                description=request.data['description'],
            )
            return success_response()
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


class CommitTransferRequest(AuthenticatedAPIView):
    def post(self, request: HttpRequest):
        try:
            transfer_services.accept_or_reject_transfer_request(
                # task_id of the transfer request to find
                task_id=request.data['ID'],
                # the new status of the transfer request
                accept=request.data['accept'] == "true"
            )
            return success_response()
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# get the transfers of a particular user
class TransferView(AuthenticatedAPIView):
    def get(self, request: HttpRequest):
        try:
            uuid = authenticate_jwt(request)

            user_uuid = uuid  # TODO:  take it from jwt
            transfer_request_list = transfer_services.get_transfer_of_user(
                user_uuid=user_uuid
            )
            serializer = TransferSerializer(
                transfer_request_list,
                many=True
            )
            return success_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# Get all transfers decreasing filter by status or creation date
class TransferAllView(AuthenticatedAPIView):
    def get(self, request: HttpRequest):
        page_size = 1
        try:
            estado = request.data['status']
            creacion = request.data['creation_date']
            transfer_request_list = transfer_services.get_all_transfers(
                status=estado, creation_date=creacion)
            serializer = TransferSerializer(
                transfer_request_list,
                many=True
            )
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(
                transfer_request_list, request)
            serializer = TransferSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# Get User all
class GetUserView(AuthenticatedAPIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest):
        try:
            user_uuid = UserSerializer(User.objects.all(), many=True).data
            if user_uuid:
                return success_response({"user_uuid": user_uuid})
            else:
                return success_response({"user_uuid": None})
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# Make a transfer to a user
class PayToUserView(AuthenticatedAPIView):

    def post(self,  request: HttpRequest):
        # Obtenemos el el uid del usuario que esta realizando la transaccion
        uuid = authenticate_jwt(request)
        isValid = is_valid_uuid(uuid)
        to_user = request.data['to_user']
        currency = request.data['currency']
        amount = request.data['amount']
        fee_amount = request.data['fee_amount']
        description = request.data['description']

        if len(currency) > 8:
            return success_response({'currency': 'Invalid currency'})
        if len(amount) > 36:
            return success_response({'amount': 'Invalid amount'})
        if len(fee_amount) > 36:
            return success_response({'fee_amount': 'Invalid fee_amount'})
        if len(description) > 256:
            return success_response({'description': 'Invalid description'})

        if isValid is True:
            try:
                task_id = transfer_services.new_transfer(
                    # transfer data
                    from_user=uuid,
                    to_user=to_user,
                    currency=currency,
                    amount=amount,
                    fee_amount=fee_amount,
                    description=description,
                )
                return success_response({'task_id': task_id})
            except Exception as e:
                Log.error(e)
                return error_response()
        else:
            return success_response({'uuid': 'Invalid uuid'})


# Conversion to currency
class GetConversionView(AuthenticatedAPIView):

    @swagger_auto_schema(operation_description="El parametro -from_user- debe ser un uuid válido y este se extrae del JWT que es enviado en el Token Authorization",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'from_user': openapi.Schema(type=openapi.TYPE_STRING),
                                 'from_asset': openapi.Schema(type=openapi.TYPE_STRING),
                                 'from_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                 'to_assets': openapi.Schema(type=openapi.TYPE_STRING),
                             }
                         ))
    def post(self,  request: HttpRequest):

        # Obtenemos el el uid del usuario que esta realizando la transaccion
        uuid = authenticate_jwt(request)

        f_asset = request.data['from_asset']
        f_amount = request.data['from_amount']
        t_asset = request.data['to_asset']
        t_fee = settings.FEE_CONFIG

        if len(f_asset) > 8:
            return success_response({'currency': 'Invalid asset'})
        if len(f_amount) > 37:
            return success_response({'currency': 'Invalid amount'})
        if len(t_asset) > 8:
            return success_response({'currency': 'Invalid asset'})

        try:
            transfer_services.get_conversion(
                from_user_uuid=uuid,
                from_asset=f_asset,
                from_amount=f_amount,
                to_asset=t_asset,
                fee_amount=t_fee,
            )
            return success_response()
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# Quote currency with request_id
class QuoteView(AuthenticatedAPIView):

    # pending conversion table BD
    @swagger_auto_schema(operation_description="parametro: request_id", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'request_id': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def post(self,  request: HttpRequest):
        uuid = authenticate_jwt(request)
        request_id = request.data['request_id']

        if is_valid_uuid(request_id):
            try:
                task_id = transfer_services.execute_conversion(
                    user_uuid=uuid,
                    request_id=request_id,
                    fee_amount=settings.FEE_CONFIG
                )
                return success_response({'task_id': task_id})
            except Exception as e:
                Log.error(traceback.format_exc())
                return error_response(e)
        else:
            return error_response(
                InvalidArgumentException('invalid request_id')
            )

    def get(self, request: HttpRequest):
        page_size = 2
        try:
            request_id = request.data['request_id']
            if not is_valid_uuid(request_id):
                return error_response(InvalidArgumentException('invalid request_id'))
            maybe_quote = transfer_services.get_quote(
                request_id=request_id)
            if maybe_quote == None:
                return error_response(QuoteNotFoundException())
            serializer = QuoteSerializer(maybe_quote)
            return success_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)


# Get all request_id
class RequestIdAllView(AuthenticatedAPIView):
    @method_decorator(cache_page(60*60*2))
    def get(self, request: HttpRequest):
        page_size = 2
        try:
            estado = request.data['status']
            creacion = request.data['creation_date']
            current_conversions = transfer_services.get_current_conversions(
                status=estado, creation_date=creacion)
            serializer = CurrentConversionSerializer(
                current_conversions,
                many=True
            )
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(
                current_conversions, request)
            serializer = CurrentConversionSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            Log.error(traceback.format_exc())
            return error_response(e)

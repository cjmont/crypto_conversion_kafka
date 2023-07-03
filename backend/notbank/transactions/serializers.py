import serpy


class UserSerializer(serpy.Serializer):
    uuid = serpy.Field(attr="uuid")
    phone = serpy.Field(attr="phone")


class TransferSerializer(serpy.Serializer):
    from_user = UserSerializer()
    to_user = UserSerializer()
    currency = serpy.Field(attr="currency")
    amount = serpy.Field(attr="amount")
    description = serpy.Field(attr="description")


class TransferRequestSerializer(serpy.Serializer):
    transfer = TransferSerializer(attr="transfer")
    status = serpy.Field(attr="status")
    task_id = serpy.Field(attr="task_id")

class CurrentConversionSerializer(serpy.Serializer):
    request_id = serpy.Field(attr="request_id")

class QuoteSerializer(serpy.Serializer):
    uuid =  serpy.Field(attr="uuid")
    request_id = serpy.Field(attr="request_id")
    from_currency = serpy.Field(attr="from_currency")
    from_amount = serpy.Field(attr="from_amount")
    to_currency = serpy.Field(attr="to_currency")
    to_amount = serpy.Field(attr="to_amount")
    perfect_amount = serpy.Field(attr="perfect_amount")
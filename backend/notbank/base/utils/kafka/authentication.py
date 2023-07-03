import hashlib
import hmac

from django.conf import settings


def hmac_sign(message: str, key: str) -> str:
    hashed = hmac.new(
        key=bytes(key, "utf-8"),
        msg=bytes(message, "utf-8"),
        digestmod=hashlib.sha256
    )
    return hashed.hexdigest()


def sign(message: str) -> str:
    return hmac_sign(message=message, key=settings.KAFKA_CELERY_KEY)


def check_valid_signature(message: str, signature: str) -> bool:
    return sign(message) == signature

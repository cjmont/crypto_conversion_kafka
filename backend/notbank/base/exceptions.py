from enum import Enum


class NotBankException(Exception):
    pass


class NotBankKafkaException(NotBankException):
    pass


class NotBankAPIException(NotBankException):
    code: int

    class STATUS(Enum):
        ERROR = 'ERROR'
        PENDING = 'PENDING'
    status: STATUS

    def __init__(self, message: str):
        super.__init__(message)

    def to_dict(self):
        return {'code': self.code, 'status': self.status.value, 'message': self.message}


class InvalidArgumentException(NotBankAPIException):
    code = 1000
    status = NotBankAPIException.STATUS.ERROR

    def __init__(self, message: str):
        self.message = message


class UserNotFoundException(NotBankAPIException):
    code = 2000
    status = NotBankAPIException.STATUS.ERROR
    message = 'User not found'

    def __init__(self):
        pass  # message is a class variable


class TransferNotFoundException(NotBankAPIException):
    code = 2001
    status = NotBankAPIException.STATUS.ERROR
    message = 'Transfer not found'

    def __init__(self):
        pass  # message is a class variable


class TransferRequestAlreadyCommitedException(NotBankAPIException):
    code = 2002
    status = NotBankAPIException.STATUS.ERROR
    message = 'Transfer request already commited'

    def __init__(self):
        pass  # message is a class variable


class TransferRequestNotFoundException(NotBankAPIException):
    code = 2003
    status = NotBankAPIException.STATUS.ERROR
    message = 'Transfer request not found'

    def __init__(self):
        pass  # message is a class variable


class ConversionAlreadyRunningException(NotBankAPIException):
    code = 2004
    status = NotBankAPIException.STATUS.ERROR
    message = 'Conversion already running'

    def __init__(self):
        pass  # message is a class variable
    

class QuoteNotFoundException(NotBankAPIException):
    code = 2005
    status = NotBankAPIException.STATUS.ERROR
    message = 'Quote not found'

    def __init__(self):
        pass  # message is a class variable


class DepositAlreadyRunningException(NotBankAPIException):
    code = 2006
    status = NotBankAPIException.STATUS.ERROR
    message = 'Deposit already running'

    def __init__(self):
        pass  # message is a class variable
    
    
class RequestIDNotFoundException(NotBankAPIException):
    code = 2007
    status = NotBankAPIException.STATUS.ERROR
    message = 'request_id for deposit not found'

    def __init__(self):
        pass  # message is a class variable
from notbank.base.exceptions import NotBankException


class TramaException(NotBankException):
    pass


class TramaFormatException(TramaException):
    pass


class TramaValidationException(TramaException):
    pass


class TramaLengthException(TramaException):
    pass

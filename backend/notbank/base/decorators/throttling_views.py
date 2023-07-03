from ratelimit.decorators import ratelimit


def ultrahigh_security(func):
    return ratelimit(group='global', key='user_or_ip', rate='10/2s', block=True)(
        ratelimit(group='global', key='user_or_ip', rate='150/m', block=True)(
            ratelimit(key='user_or_ip', rate='10/m', block=True)(
                ratelimit(key='user_or_ip', rate='30/h', block=True)(
                    ratelimit(key='user_or_ip', rate='60/d', block=True)(func)
                )
            )
        )
    )


def high_security_nonblocking(func):
    return ratelimit(group='global', key='user_or_ip', rate='10/2s')(
        ratelimit(group='global', key='user_or_ip', rate='150/m')(
            ratelimit(key='user_or_ip', rate='20/m')(
                ratelimit(key='user_or_ip', rate='60/h')(
                    ratelimit(key='user_or_ip', rate='120/d')(func)
                )
            )
        )
    )


def high_security(func):
    return ratelimit(group='global', key='user_or_ip', rate='10/2s', block=True)(
        ratelimit(group='global', key='user_or_ip', rate='150/m', block=True)(
            ratelimit(key='user_or_ip', rate='20/m', block=True)(
                ratelimit(key='user_or_ip', rate='60/h', block=True)(
                    ratelimit(key='user_or_ip', rate='120/d', block=True)(func)
                )
            )
        )
    )


def standard_security_nonblocking(func):
    return ratelimit(group='global', key='user_or_ip', rate='10/2s')(
        ratelimit(group='global', key='user_or_ip', rate='150/m')(
            ratelimit(key='user_or_ip', rate='20/m')(
                ratelimit(key='user_or_ip', rate='500/h')(func)
            )
        )
    )


def standard_security(func):
    return ratelimit(group='global', key='user_or_ip', rate='10/2s', block=True)(
        ratelimit(group='global', key='user_or_ip', rate='150/m', block=True)(
            ratelimit(key='user_or_ip', rate='20/m', block=True)(
                ratelimit(key='user_or_ip', rate='500/h', block=True)(func)
            )
        )
    )


def standardstaff_security(func):
    return ratelimit(group='global', key='user_or_ip', rate='150/m', block=True)(
        ratelimit(key='user_or_ip', rate='60/m', block=True)(func)
    )


def low_security(func):
    return ratelimit(key='user_or_ip', rate='300/m', block=True)(func)

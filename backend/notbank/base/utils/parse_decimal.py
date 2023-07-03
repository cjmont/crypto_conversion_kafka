# -*- coding: UTF-8 -*-

from decimal import Decimal


def truncate(val, decimals):
    exp = 10**decimals
    return Decimal(int(val * exp)) / Decimal(exp)


def dec_to_str(val):
    if val == 0 or val is None:
        return '0'
    return str(val)


def dec_to_str_striped(val):
    if val == 0 or val is None:
        return '0'
    dec_str = val
    if not isinstance(val, str):
        dec_str = '{0:f}'.format(val)
    return dec_str.rstrip('0').rstrip('.') if '.' in dec_str else dec_str


def dec_to_str_fixed_point(val: Decimal, fixed_point_count: int) -> str:
    '''
        Returns the decimal as string with fixed count of fixed points.

        Example:
            
            print(dec_to_str_fixed_point(Decimal(20), 3))
            20.000
    '''
    return ('{:10.'+str(fixed_point_count)+'f}').format(val).strip()


def round_dec_to_str(val, decimals):
    if val == 0 or val is None:
        return '0'
    rounded = truncate(val, decimals)
    if decimals == 0:
        return str(int(rounded))
    return str(rounded)


def round_keep_dec_to_str(val, decimals):
    if val == 0 or val is None:
        return '0'
    rounded = truncate(val, decimals)
    if decimals == 0:
        return str(int(rounded))

    f = '{0:.' + str(decimals) + 'f}'
    dec_str = f.format(rounded)
    return dec_str


def round_dec(val, decimals):
    if val == 0 or val is None:
        return int(0)
    rounded = truncate(val, decimals)
    if decimals == 0:
        return int(rounded)
    return rounded


def base_round(x, base):
    return base * truncate(x/base, 0)

from .cache import get_base_currency_factors, get_active_currency
import logging
from .get_current_tenant import get_current_tenant


def get_current_tenant_currency_code() -> str:
    tenant = get_current_tenant()
    return tenant.currency_code.lower()


def get_currency_code_factor(code) -> float:
    tenant_code = get_current_tenant_currency_code()
    factor = get_base_currency_factors(
        tenant_code
    )[tenant_code][code.lower()]
    return factor    


def get_active_currency_code(*args, **kwargs) -> str:
    _active_currency = get_active_currency()
    if _active_currency is not None:
        return _active_currency['currency_code'].lower()
    return get_current_tenant_currency_code()


def currency_converter(price, currency_code=None):
    """convert price from tenant default currency to the required currency"""
    if currency_code is None:
        currency_code = get_current_tenant_currency_code()
    try:
        factor = get_currency_code_factor(currency_code)
        return  factor * price
    except Exception as e:
        print("excption here", e)
        logging.warning(f"ops, price converter failed : {e}")
        return price


def price_converter(price):
    try:
        _active_currency = get_active_currency()
        if _active_currency is not None:
            active_currency_code = _active_currency['currency_code'].lower()
            factor = get_currency_code_factor(active_currency_code)
            return  factor * price
        return price
    except Exception as e:
        print("excption here", e)
        logging.warning(f"ops, price converter failed : {e}")
        return price
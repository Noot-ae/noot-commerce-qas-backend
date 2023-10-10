from rest_framework.exceptions import ValidationError

class OrderSoldException(ValidationError):
    default_code = "order_already_paid"
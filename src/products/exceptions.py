class BaseException(Exception):
    message = ""


class ProductOutOfStockException(BaseException):
    message = "This product is out of stock."

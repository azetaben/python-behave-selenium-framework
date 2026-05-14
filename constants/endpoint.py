"""Endpoint constants for route-level assertions/navigation."""

from enum import Enum


class EndPoint(str, Enum):
    LOGIN = "/"
    INVENTORY = "/inventory.html"
    CART = "/cart"
    CHECKOUT_STEP_ONE = "/checkout-step-one"
    CHECKOUT_STEP_TWO = "/checkout-step-two"
    CHECKOUT_COMPLETE = "/checkout-complete"


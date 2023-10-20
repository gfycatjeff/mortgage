# constants.py

from enum import Enum, auto

class PaymentSchedule(Enum):
    ACCELERATED_BIWEEKLY = "accelerated_biweekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"

    @staticmethod
    def list():
        return list(map(lambda c: c.name, PaymentSchedule))

# Constraints
DOWN_PAYMENT_PERCENTAGE = 0.2
PROPERTY_PRICE_MIN = 0
ANNUAL_INTEREST_MIN = 0

# Error messages
PROPERTY_PRICE_MIN_ERROR = "Property price must be greater than zero."
DOWN_PAYMENT_ERROR = "Down payment must be at least 20% of the property price."
DOWN_PAYMENT_MAX_ERROR = "Down payment must not be greater than the property price."
INVALID_SCHEDULE_ERROR = "Invalid payment schedule. Please choose from 'accelerated bi-weekly', 'bi-weekly', or 'monthly'."
ANNUAL_INTEREST_ERROR = "Annual interest rate must be non-negative."
AMORTIZATION_PERIOD_ERROR = "Amortization period must be greater than zero, less than or equal to 30, and in 5 year increments."

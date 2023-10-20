# test_main.py

import pytest
from main import mortgage_calculator
import constants

def test_mortgage_calculator_success():
    payment = mortgage_calculator(
        property_price=500000,
        down_payment=100000,
        annual_interest_rate=5,
        amortization_period=30,
        payment_schedule=constants.PaymentSchedule.MONTHLY
    )
    assert payment == 2147.29

def test_mortgage_calculator_low_down_payment():
    with pytest.raises(ValueError) as excinfo:
        mortgage_calculator(
            property_price=500000,
            down_payment=50000,
            annual_interest_rate=5,
            amortization_period=30,
            payment_schedule=constants.PaymentSchedule.MONTHLY
        )
    assert str(excinfo.value) == constants.DOWN_PAYMENT_ERROR

def test_mortgage_calculator_invalid_schedule():
    with pytest.raises(ValueError) as excinfo:
        mortgage_calculator(
            property_price=500000,
            down_payment=100000,
            annual_interest_rate=5,
            amortization_period=30,
            payment_schedule="weekly",
        )
    assert str(excinfo.value) == constants.INVALID_SCHEDULE_ERROR

def test_mortgage_calculator_zero_interest_rate():
    payment = mortgage_calculator(
        property_price=500000,
        down_payment=100000,
        annual_interest_rate=0,
        amortization_period=30,
        payment_schedule=constants.PaymentSchedule.MONTHLY,
    )
    assert payment == 1111.11  # calculated value with 0% interest rate

def test_biweekly_vs_accelerated_biweekly():
    property_price = 500000
    down_payment = 100000
    annual_interest_rate = 5
    amortization_period = 25

    biweekly_payment = mortgage_calculator(
        property_price,
        down_payment,
        annual_interest_rate,
        amortization_period,
        constants.PaymentSchedule.BIWEEKLY,
    )

    accelerated_biweekly_payment = mortgage_calculator(
        property_price,
        down_payment,
        annual_interest_rate,
        amortization_period,
        constants.PaymentSchedule.ACCELERATED_BIWEEKLY,
    )

    assert accelerated_biweekly_payment > biweekly_payment, "Accelerated bi-weekly payment should be more than bi-weekly payment"


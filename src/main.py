# main.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
import constants

app = FastAPI()

# Error validation
def validate_inputs(
    property_price: float,
    down_payment: float,
    annual_interest_rate: float,
    amortization_period: int,
    payment_schedule: constants.PaymentSchedule,
):
    if property_price <= constants.PROPERTY_PRICE_MIN:
        raise ValueError(constants.PROPERTY_PRICE_MIN_ERROR)

    if down_payment < property_price * constants.DOWN_PAYMENT_PERCENTAGE:
        raise ValueError(constants.DOWN_PAYMENT_ERROR)

    if down_payment > property_price:
        raise ValueError(constants.DOWN_PAYMENT_MAX_ERROR)

    if annual_interest_rate < constants.ANNUAL_INTEREST_MIN:
        raise ValueError(constants.ANNUAL_INTEREST_ERROR)

    if amortization_period <= 0 or amortization_period > 30 or amortization_period % 5 != 0:
        raise ValueError(constants.AMORTIZATION_PERIOD_ERROR)

# Testable, re-usable mortgage calculation function
def mortgage_calculator(
    property_price: float,
    down_payment: float,
    annual_interest_rate: float,
    amortization_period: int,
    payment_schedule: constants.PaymentSchedule,
):
    validate_inputs(
        property_price, down_payment,
        annual_interest_rate, amortization_period, payment_schedule)

    principal = property_price - down_payment
    payments_per_annum = 12  # default
    if payment_schedule == constants.PaymentSchedule.ACCELERATED_BIWEEKLY:
        payments_per_annum = 26
        effective_annual_payments = 24
    elif payment_schedule == constants.PaymentSchedule.BIWEEKLY:
        payments_per_annum = 26
    elif payment_schedule == constants.PaymentSchedule.MONTHLY:
        payments_per_annum = 12
    else:
        raise ValueError(constants.INVALID_SCHEDULE_ERROR)

    interest_rate_per_payment = annual_interest_rate / 100 / payments_per_annum
    total_payments = amortization_period * payments_per_annum

    # Avoid divide by zero error-- optional to reject input
    if annual_interest_rate == 0:
        payment_per_schedule = principal / total_payments
    else:
        payment_per_schedule = (
            principal
            * interest_rate_per_payment
            * (1 + interest_rate_per_payment) ** total_payments
        ) / ((1 + interest_rate_per_payment) ** total_payments - 1)

    if payment_schedule == constants.PaymentSchedule.ACCELERATED_BIWEEKLY:
        payment_per_schedule = payment_per_schedule * payments_per_annum / effective_annual_payments

    return round(payment_per_schedule, 2)


# Mount the static files for html UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# External API
@app.get("/mortgage_calculator")
async def mortgage_calculator_endpoint(
    property_price: float = Query(
        ..., title="Property Price",
        description="The price of the property."),
    down_payment: float = Query(
        ..., title="Down Payment",
        description="The down payment made on the property."),
    annual_interest_rate: float = Query(
        ..., title="Annual Interest Rate",
        description="The annual interest rate on the mortgage."),
    amortization_period: int = Query(
        ..., title="Amortization Period",
        description="The amortization period of the mortgage in years.",
        ge=5, le=30),
    payment_schedule: str = Query(
        ..., title="Payment Schedule",
        description="The payment schedule for the mortgage, "
                    "either 'accelerated bi-weekly', 'bi-weekly', or 'monthly'."),
):
    if payment_schedule is None:
        raise HTTPException(
            status_code=400, detail="Payment schedule is required")
    if payment_schedule.upper() not in constants.PaymentSchedule.list():
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payment schedule. Please choose from "
                   f"{constants.PaymentSchedule.list()}")
    payment_schedule_enum = constants.PaymentSchedule(payment_schedule.lower())

    try:
        payment = mortgage_calculator(
            property_price, down_payment,
            annual_interest_rate, amortization_period,
            payment_schedule_enum)
        return {"payment_per_schedule": payment}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

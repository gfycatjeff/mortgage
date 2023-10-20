# Mortgage Calculator

A simple FastAPI application for calculating mortgage payments.

## Running the Project

### Using Docker

1. Build the Docker image:

    ```sh
    docker build -t mortgage_calculator .
    ```

2. Run the Docker container:

    ```sh
    docker run -d --name mortgage_calculator -p 8000:8000 mortgage_calculator
    ```

### Using Python Directly

1. Install the requirements:

    ```sh
    pip install -r requirements.txt
    ```

2. Run the FastAPI server:

    ```sh
    uvicorn main:app --reload
    ```

### Running the Tests

```sh
pytest
```

## Using the API

### With cURL

Replace the following placeholders in the examples below:

- `<property_price>`
- `<down_payment>`
- `<annual_interest_rate>`
- `<amortization_period>`
- `<payment_schedule>`

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/mortgage_calculator?property_price=<property_price>&down_payment=<down_payment>&annual_interest_rate=<annual_interest_rate>&amortization_period=<
```

With WebUI

Once the application is running, you can also use the web interface to calculate mortgage payments. Open your browser and navigate to http://127.0.0.1:8000/static to access the UI.


async function calculate(event) {
    event.preventDefault();
    const propertyPrice = document.getElementById('propertyPrice').value;
    const downPayment = document.getElementById('downPayment').value;
    const annualInterestRate = document.getElementById('annualInterestRate').value;
    const amortizationPeriod = document.getElementById('amortizationPeriod').value;
    const paymentSchedule = document.getElementById('paymentSchedule').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/mortgage_calculator?property_price=${propertyPrice}&down_payment=${downPayment}&annual_interest_rate=${annualInterestRate}&amortization_period=${amortizationPeriod}&payment_schedule=${paymentSchedule}`);

        const data = await response.json();

        if (response.status === 400) {
            document.getElementById('error').innerText = data.detail;
            document.getElementById('result').innerText = '';
        } else {
            document.getElementById('result').innerText = data.payment_per_schedule;
            document.getElementById('error').innerText = '';
        }
    } catch (error) {
        document.getElementById('error').innerText = 'Error calculatng mortgage. Please check the API.';
    }
}

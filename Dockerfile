FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Should likely be separated out to a different part of CI/CD
RUN pytest


# Launch FastAPI using uvicorn (can use --reload and share a volume to monitor for source changes) 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENV clientID
ENV redirect_us_uri

CMD ["python", "run-api.py"]

FROM python:3.12.9-alpine3.21

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/app"]

ARG CLIENTID_ARG

ARG REDIRECT_US_URI_ARG

ENV clientID=$CLIENTID_ARG

ENV redirect_us_uri=$REDIRECT_US_URI_ARG

CMD ["python", "run-api.py"]

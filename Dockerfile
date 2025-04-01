FROM python:3.12.9-alpine3.21

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/app"]

ARG CLIENT_ID_ARG
ARG REDIRECT_YANDEX_ARG
ARG OUR_URL_ARG

ENV CLIENT_ID=$CLIENT_ID_ARG
ENV REDIRECT_YANDEX=$REDIRECT_YANDEX_ARG
ENV OUR_URL=$OUR_URL_ARG

CMD ["python", "run-api.py"]

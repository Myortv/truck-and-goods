FROM python:3.11

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./prestart.sh /app/
COPY ./app/ /app/app/
COPY ./uszips.csv /app/app/data/uszips.csv

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["/app/prestart.sh"]


FROM python:3.12.4-bookworm

RUN apt update -y
RUN apt install python3-dev libpq-dev -y

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN cp configs.sample.py configs.py

EXPOSE 8000

# gunicron configs is gunicorn.conf.py
CMD ["gunicorn", "bitArticles.wsgi:application"]

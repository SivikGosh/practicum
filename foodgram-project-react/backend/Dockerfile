FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install -r req.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
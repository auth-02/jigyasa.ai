FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]

FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 8080 2222 3306
CMD ["python", "src/app.py"]

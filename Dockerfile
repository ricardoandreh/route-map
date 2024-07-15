FROM docker.io/python:3.10.12-alpine3.18

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

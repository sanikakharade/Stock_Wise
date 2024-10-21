FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ARG DJANGO_ALLOWED_HOSTS
ARG SECRET_KEY
ARG SUPABASE_DB_NAME
ARG SUPABASE_DB_USER
ARG SUPABASE_PASSWORD
ARG SUPABASE_HOST
ARG SUPABASE_PORT
ARG ALPHA_VANTAGE_API_KEY

ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS \
    SECRET_KEY=$SECRET_KEY \
    SUPABASE_DB_NAME=$SUPABASE_DB_NAME \
    SUPABASE_DB_USER=$SUPABASE_DB_USER \
    SUPABASE_PASSWORD=$SUPABASE_PASSWORD \
    SUPABASE_HOST=$SUPABASE_HOST \
    SUPABASE_PORT=$SUPABASE_PORT \
    ALPHA_VANTAGE_API_KEY=$ALPHA_VANTAGE_API_KEY

COPY . /app/

RUN python manage.py makemigrations

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

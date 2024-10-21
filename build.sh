#!/bin/bash

set -a
source .env
set +a

docker build \
  --build-arg DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}" \
  --build-arg SECRET_KEY="${SECRET_KEY}" \
  --build-arg SUPABASE_DB_NAME="${SUPABASE_DB_NAME}" \
  --build-arg SUPABASE_DB_USER="${SUPABASE_DB_USER}" \
  --build-arg SUPABASE_PASSWORD="${SUPABASE_PASSWORD}" \
  --build-arg SUPABASE_HOST="${SUPABASE_HOST}" \
  --build-arg SUPABASE_PORT="${SUPABASE_PORT}" \
  --build-arg ALPHA_VANTAGE_API_KEY="${ALPHA_VANTAGE_API_KEY}" \
  -t stockwise .

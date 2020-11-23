#!/bin/bash -x

alembic revision --autogenerate -m "create tables in database"
alembic upgrade head

uvicorn app.main:app --reload --host 0.0.0.0

exec "$@"
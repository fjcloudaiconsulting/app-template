# syntax=mirror.gcr.io/docker/dockerfile:1
FROM mirror.gcr.io/library/python:3.13-slim@sha256:bb2988715db2cf7ace7b53f38f3cffbef7c7046a656bee66245eb0ed386e2e81 AS prod
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY app.py .
# Build-time only; the shared build-image workflow passes exactly these ARG names. Keep them when renaming
# the app prefix and map them to your own ENV names instead.
ARG APP_VERSION
ARG APP_REVISION
ENV APP_VERSION=$APP_VERSION \
    APP_REVISION=$APP_REVISION \
    PYTHONUNBUFFERED=1
USER app
EXPOSE 8000
CMD ["python","app.py"]

# Placeholder: replace with the project's migration tool. Must be idempotent (the smoke test runs it twice).
FROM prod AS migrations
CMD ["true"]

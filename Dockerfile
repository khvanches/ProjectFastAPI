  FROM python:3.13

    RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

    WORKDIR /code

    COPY pyproject.toml poetry.lock* /code/

    RUN poetry config virtualenvs.create false \
        && poetry install --no-root --no-interaction --no-ansi

    COPY ./app /code/app

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
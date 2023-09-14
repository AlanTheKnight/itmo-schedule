FROM python:3.11

# Set the working directory to /backend
WORKDIR /backend

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /backend/

# Install poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /backend/

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "backend.wsgi:application"]

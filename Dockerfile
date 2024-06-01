FROM python:3.11

# Set the working directory
WORKDIR /chatters-app

# Copy local code to the container image
COPY pyproject.toml poetry.lock README.md .env ./

# Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only=main

EXPOSE 8000

COPY ./app ./app

# Run the web service on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
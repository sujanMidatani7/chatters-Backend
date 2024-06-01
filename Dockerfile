FROM python:3.12

# Set the working directory
WORKDIR /chatters-app

COPY . .

# Copy local code to the container image
# COPY pyproject.toml poetry.lock .env ./


# # Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only=main

EXPOSE 8000



COPY start.sh ./

RUN chmod +x ./start.sh
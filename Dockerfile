FROM python:3.12

# Set the working directory
WORKDIR /chatters-app

COPY . .

# Copy local code to the container image
# COPY pyproject.toml poetry.lock .env ./


# # Install dependencies using Poetry
RUN pip install -r requirements.txt

EXPOSE 8001



COPY start.sh ./

RUN chmod +x ./start.sh
FROM python:3.12

# Set the working directory
WORKDIR /chatters-app

COPY . .

# Copy local code to the container image
# COPY pyproject.toml poetry.lock .env ./


#
RUN pip install -r requirements.txt

EXPOSE 8001



COPY start.sh ./

RUN chmod +x ./start.sh

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8001"]
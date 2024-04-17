FROM python:3.8-slim-buster

WORKDIR /app

COPY ./ ./

RUN python3 -m pip install -r requirements.txt

# Expose the listening port
EXPOSE 8000

# Run npm start script when container starts
CMD [ "python3", "-m", "app" ]

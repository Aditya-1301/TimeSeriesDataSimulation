FROM python:3.8-slim

# Install locust
RUN pip install locust

# Set the working directory
WORKDIR /usr/src/app

# Copy the script and locustfile into the container
COPY locustfile.py .
COPY script.py .

# The entrypoint runs the script
ENTRYPOINT ["python3", "script.py"]

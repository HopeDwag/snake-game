# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
# WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP app/main.py

# Expose the port that the Flask app will run on
EXPOSE 8080

RUN echo "my-hostname" > /etc/hostname
# Start the Flask app
CMD [ "flask", "run", "--port=8080", "--host=0.0.0.0" ]
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the desired port (e.g., 8000 if it's a web application)
# EXPOSE 8000

# Define the command to run your application
# CMD ["python", "consumer.py"]
CMD ["python", "consumer.py"]

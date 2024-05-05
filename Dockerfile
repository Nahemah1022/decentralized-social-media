# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the src directory into the container
COPY src/ ./src

# Make port available to the world outside this container
EXPOSE 8000 9000 9001 9002 9003 6000 6001 6002 6003

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"]

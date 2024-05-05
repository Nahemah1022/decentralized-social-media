# Stage 1: Build the React application
FROM node:latest as react-build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build


# Stage 2: Setup the Python environment and copy the React build output
FROM python:3.9-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the src directory into the container
COPY src/ ./src
COPY --from=react-build /app/build ./frontend/build

# Make port available to the world outside this container
EXPOSE 8000 9000 9001 9002 9003 6000 6001 6002 6003

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"]

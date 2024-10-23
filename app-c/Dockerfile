# Use a smaller base image for Python
FROM python:3.10-slim as base

# Create a directory for the app and switch to a non-root user
WORKDIR /usr/src/app

# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Expose the port the application runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app_c.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

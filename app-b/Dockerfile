# Use a lighter Python base image to minimize image size
FROM python:3.10-slim

# Install necessary utilities and dependencies
RUN apt-get update && apt-get install -y \
    curl telnet iputils-ping locales \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Set the environment for locale
ENV LANG=en_US.utf8

# Create a non-root user for security
RUN useradd -ms /bin/bash appuser

# Switch to non-root user
USER appuser

# Create a directory for the app
WORKDIR /app

# Copy requirements.txt first to leverage Docker layer caching
COPY --chown=appuser:appuser ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application source code as non-root user
COPY --chown=appuser:appuser . /app

# Expose the port the application runs on
EXPOSE 5000

# Run the application
CMD ["python3", "app_b.py"]
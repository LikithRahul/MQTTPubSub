# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY publisher.py subscriber.py /app/

# Install required Python packages
RUN pip install requests paho-mqtt

# Expose ports for MQTT communication
EXPOSE 1883

# Default command (start publisher)
CMD ["python", "publisher.py"]
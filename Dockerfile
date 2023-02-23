# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 80 for the Flask app
EXPOSE 80

# Run the Python app with the gunicorn server
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]

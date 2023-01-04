# Start from the latest version of Python
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the source code to the working directory
COPY . .

# Expose port 5000 to the host
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP app.py

# Run the application when the container is started
CMD ["flask", "run", "--host=0.0.0.0"]
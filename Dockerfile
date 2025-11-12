# Use official Python image as base
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port (Cloud Run default is 8080)
EXPOSE 8080

# Set environment variable for Flask (if using Flask)
ENV FLASK_APP=run.py

# Command to run the app (adjust if using something other than Flask)
CMD ["python", "run.py"]

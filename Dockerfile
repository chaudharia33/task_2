# Use an official Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the application code
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port the FastAPI service will run on
EXPOSE 8000

# Run the command to start the FastAPI service when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
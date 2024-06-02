# Use an official Python runtime as a parent image
FROM python:3.9
 
# Set the working directory to /app
WORKDIR /app
 
# Copy the requirements file into the container at /app
COPY requirements.txt /app/
 
# Install the required dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of the application code to the container
COPY . /app/
 
# Expose the port on which FastAPI will run
EXPOSE 8000
 
# Define the command to start the FastAPI application
CMD ["python", "/app/main.py"]
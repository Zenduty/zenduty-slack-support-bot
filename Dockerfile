# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to the working directory in the container
COPY . /code

# Command to run the application 
# CMD ["bash", "-c", "python -u -m flask run --host=0.0.0.0 --port=$APP_PORT"]
CMD ["bash", "-c", "python app.py"]

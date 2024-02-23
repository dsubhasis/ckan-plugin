# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install python-dotenv and asyncpg
RUN pip install fastapi uvicorn python-dotenv asyncpg

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

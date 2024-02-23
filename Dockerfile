# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container


# Install python-dotenv and asyncpg
WORKDIR /app
COPY ./requirements.txt  /app/requirements.txt
COPY . /app
RUN pip install  --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

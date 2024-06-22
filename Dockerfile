# Use an official Python runtime as a parent image
FROM python:3.11-slim
#FROM arm64v8/python:3.11-slim

# Set the working directory in the container
WORKDIR /app
  
# Install ffmpeg
RUN apt-get update -qq && apt-get install -y ffmpeg || (cat /var/log/apt/* && false)

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Run bot.py when the container launches
CMD ["python", "main.py"]

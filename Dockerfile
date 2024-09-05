# Use an official Python runtime as a parent image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    fontconfig \
    libfreetype6-dev \
    libsdl2-ttf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run tic_tac_toe_ai.py when the container launches
CMD ["python", "tic_tac_toe_ai.py"]
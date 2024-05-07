FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Run app.py when the container launches, using the PORT environment variable
CMD ["sh", "-c", "python app.py"]

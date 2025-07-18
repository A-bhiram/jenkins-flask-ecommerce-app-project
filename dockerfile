# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]

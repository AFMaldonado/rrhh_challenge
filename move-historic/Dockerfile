FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY . /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

CMD ["python3", "main.py"]
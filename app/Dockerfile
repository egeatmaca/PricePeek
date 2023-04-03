FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy the rest of the files to the working directory
COPY . .

# Run the main.py file
CMD ["python", "main.py"]
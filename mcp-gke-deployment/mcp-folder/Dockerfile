FROM python:3.11-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py server_old.py server_gke.py .

# Expose port (matches FastMCP default)
EXPOSE 8080

# Run the server
CMD ["python", "server_gke.py"]
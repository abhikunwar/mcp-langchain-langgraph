FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    langgraph \
    requests \
    typing-extensions

# Copy your LangGraph application
COPY simple_langgraph_app.py .

# Run the application
CMD ["python", "simple_langgraph_app.py"]
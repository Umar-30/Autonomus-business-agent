FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Streamlit port
EXPOSE 7860

# Run the application
ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=7860", "--server.address=0.0.0.0"]

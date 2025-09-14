FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make src available (so imports like "from src..." work)
ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]

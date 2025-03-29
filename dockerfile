FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Explicitly expose the port
EXPOSE 8080

CMD ["python", "snake.py"]  # Ensure this starts your app

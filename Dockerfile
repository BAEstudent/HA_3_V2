FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port (FastAPI default is 8000)
EXPOSE 8000

# Start the app with Uvicorn
CMD python src/main.py
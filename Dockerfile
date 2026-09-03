FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5011

#CMD ["python", "run.py"]

# Lancement via Gunicorn avec la Factory Flask
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:5011", "app:create_app()"]
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DB_FILE=/data/monitor.db
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY monitor.py dashboard.py ./
CMD ["python","monitor.py"]

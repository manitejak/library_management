FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:create_app()"]

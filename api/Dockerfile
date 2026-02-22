FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN R -e "install.packages(c('tidymodels','jsonlite'), repos='https://cloud.r-project.org')"

COPY app.py .
COPY routes /app/routes
COPY middleware /app/middleware
COPY data /app/data

EXPOSE 5000

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]

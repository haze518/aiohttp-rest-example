FROM python:3.8

WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONBUFFERED=1

COPY . /app/

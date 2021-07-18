FROM python:3.8

ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_HOST

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY run.py .

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}
CMD ["python", "run.py"]
FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app
COPY algo.py /app

CMD ["python", "main.py"]

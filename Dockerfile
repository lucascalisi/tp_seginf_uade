FROM python:3.7

ADD requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app
CMD ["python3", "runner.py"]

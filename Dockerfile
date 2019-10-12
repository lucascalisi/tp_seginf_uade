FROM python:3.7
ENV PATH_APP_CA_FILES=/CA_FILES
ADD requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /
WORKDIR /
ADD . /
CMD ["python3", "runner.py"]

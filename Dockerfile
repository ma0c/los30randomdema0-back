FROM python:3.12-slim

# Set the working directory
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/


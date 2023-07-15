FROM python:3.10.6

RUN mkdir /app

COPY requirements.txt /app/

COPY . /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "core.py"]
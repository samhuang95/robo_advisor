FROM python:slim

ADD ./requirements.txt /
ADD ./app /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
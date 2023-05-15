FROM python:slim

ADD ./requirements.txt /
ADD ./app /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
# RUN apt-get update && apt-get install -y wget
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

EXPOSE 5000

CMD ["python", "app.py"]

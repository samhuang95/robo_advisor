FROM python:3.10-slim

# COPY ./cronjob /etc/cron.d/
COPY ./requirements.txt /
COPY ./app/ /app/
WORKDIR /app

# 安裝chrome
# RUN apt-get update && apt-get install -y wget
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# 安裝Chrome驅動程式
# RUN apt-get update && apt-get install -y unzip
# RUN wget -q https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip -O /tmp/chromedriver.zip
# RUN unzip /tmp/chromedriver.zip -d /usr/local/bin
# RUN rm /tmp/chromedriver.zip

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
# RUN apt-get update && apt-get install -y cron

EXPOSE 5000

# CMD cron & python app.py
CMD python app.py

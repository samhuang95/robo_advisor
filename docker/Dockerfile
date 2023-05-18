FROM python:slim


COPY start.sh .
COPY ./app/app.py .
COPY ./app/plant_kpi.py .
COPY ./root /var/spool/cron/crontabs/
COPY ./requirements.txt /
COPY ./app /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN apt-get update && apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

EXPOSE 5000

CMD ["bash", "start.sh"]
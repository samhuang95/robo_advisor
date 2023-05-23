FROM python:3.10-slim

COPY ./requirements.txt /
COPY . /app
WORKDIR /app

<<<<<<< HEAD

=======
>>>>>>> 839d16979bb76e8c042abe6e0481c65526c26086
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y build-essential \
    && apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb --fix-missing
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

EXPOSE 5000

# CMD ["bash", "start.sh"]
<<<<<<< HEAD
CMD ["python", "app.py"]
=======
CMD ["python", "app.py"]
>>>>>>> 839d16979bb76e8c042abe6e0481c65526c26086

FROM python:3.11

RUN apt-get update && apt-get install -y cron nano supervisor
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ADD supervisord.conf /etc/supervisor/conf.d/


EXPOSE 8000

CMD ["/usr/bin/supervisord"]



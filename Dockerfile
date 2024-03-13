FROM python:3.11.4-slim

WORKDIR /app

# ADD cronfile /etc/cron.d/cron-hello
# RUN chmod 0644 /etc/cron.d/cron-hello
# RUN touch /var/log/cron.log

RUN apt-get update && apt-get -y install cron && apt-get install vim -y
# RUN crontab /etc/cron.d/cron-hello
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app

CMD ["/bin/bash", "script.sh"]
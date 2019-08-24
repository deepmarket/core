FROM python:3.6.8-stretch

# Set up crontab to run service daily
# See https://stackoverflow.com/a/37458519/4668680 for more info
RUN apt-get update && apt-get -y install cron
COPY gen-prices-cron /etc/cron.d/gen-prices-cron
RUN chmod 0644 /etc/cron.d/gen-prices-cron
RUN crontab /etc/cron.d/gen-prices-cron
RUN touch /var/log/cron.log

RUN mkdir -p /core/generate

WORKDIR /core/generate

COPY . /core/generate/

RUN python -m pip install -r requirements.txt

# tail -f keeps container running
CMD cron && tail -f /dev/null
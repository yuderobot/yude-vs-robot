FROM python:3.8.11-alpine3.13
ADD ./app /app

WORKDIR /app
RUN pip install -r requirements.txt

# Add script to crontab
RUN echo '0 */12 * * * cd /app; python main.py' > /var/spool/cron/crontabs/root

ENTRYPOINT ["crond", "-f"]

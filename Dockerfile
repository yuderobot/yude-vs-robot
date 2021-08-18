FROM python:latest
ADD ./app /app

WORKDIR /app

# Install cron
RUN apt update; apt install -y cron

# Install Python dependencies
RUN pip install -r requirements.txt

# Add script to crontab
RUN echo '0 */12 * * * cd /app; python main.py' >> /etc/crontab
RUN chmod 0644 /etc/cron.d/yude-vs-robot

CMD cron && tail -f /dev/null

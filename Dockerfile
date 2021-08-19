FROM python:latest
ADD ./app /app

WORKDIR /app

# Install cron
RUN apt update; apt install -y cron

# Install Python dependencies
RUN pip install -r requirements.txt

# Add script to crontab
RUN echo '0 */12 * * * root cd /app; /usr/local/bin/python main.py' >> /etc/crontab

CMD cron && tail -f /dev/null

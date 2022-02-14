FROM python:latest
WORKDIR /app

# Install cron
RUN apt update; apt install -y cron
# Install Python dependencies
ADD ./app/requirements.txt /app/
RUN pip install -r requirements.txt
# Add script to crontab
RUN echo '0 */12 * * * root cd /app; /usr/local/bin/python main.py' >> /etc/crontab
# Add application to the image
ADD ./app/main.py /app/

CMD cron && tail -f /dev/null

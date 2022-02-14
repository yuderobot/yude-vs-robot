FROM python:3.10.2-alpine3.15
WORKDIR /app

# Setup timezone & install cron
RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

# Install Python dependencies
ADD ./app/requirements.txt /app/
RUN pip install -r requirements.txt
# Add script to crontab
RUN echo '0 */12 * * * root cd /app; /usr/local/bin/python main.py' >> /etc/crontab
# Add application to the image
ADD ./app/main.py /app/

CMD crond -l 2 -f
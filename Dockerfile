FROM python:3.9.10-alpine3.15 AS builder
WORKDIR /app

# Install Python dependencies
ADD ./app/requirements.txt /app/
RUN apk add --no-cache build-base freetype-dev jpeg-dev zlib-dev && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.9.10-alpine3.15 AS runner
WORKDIR /app

# Add script to crontab
RUN echo '0 */12 * * * root cd /app; /usr/local/bin/python main.py' >> /etc/crontab
# Setup timezone & install cron
RUN apk --update add tzdata libstdc++ freetype-dev jpeg-dev && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*
# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Add application to the image
ADD ./app/main.py /app/

CMD crond -l 2 -f
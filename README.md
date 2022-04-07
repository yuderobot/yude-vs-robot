# yude-vs-robot
🆚 Compare tweet counts of @yude_jp and @yuderobot

## Setup
1. Create `docker-compose.yml` and paste the below and set your token in this file.
    ```
    version: '3'
    services:
        app:
          restart: always
          container_name: yude-vs-robot
          image: ghcr.io/yuderobot/yude-vs-robot:main
          volumes:
            - "./data:/app/data"
          environment:
            # Twitter API related
            - CK=
            - CS=
            - AT=
            - AS=
    ```
2. Run `docker-compose up -d`. To update, run `docker-compose pull` before firing up the container.

## License
This repository is provided under the MIT License.

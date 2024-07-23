# Los 30 Random de Ma0 - Backend

If you're watching this readme that means that you're super curious and your curiosity is well received here.

If you want to contribute, you know the drill.

## Run project
This project is built on top of docker and docker-compose

To run:

```shell
docker-compose up
```

Migrations needs to be run manually so

```shell
docker exec -it los30randomdema0-back-web-1 bash
./manage.py migrate
```

To live debug endpoints

```shell
docker-compose up -d
docker rm -f los30randomdema0-back-web-1
docker-compose run --rm --service-ports web
```
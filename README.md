# REST API example using aiohttp

## How to run
Run
~~~~
$ make build
~~~~
~~~~
$ make compose-start
~~~~
## Start tests
~~~~
$ docker-compose exec -e Testing=True app pytest -x -vv
~~~~
## Swagger

~~~~
http://localhost:8080/docs
~~~~

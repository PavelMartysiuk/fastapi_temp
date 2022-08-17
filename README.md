# Fast API template

Fast API template with alembic, sqlalchemy, async tests and linters



## Getting Started

### Project setup

```shell
$ cd fastapi_temp/
$ git checkout develop
$ make install
$ make docker-up
$ make migrate
```

### Testing

Run test env:

```shell
$ make docker-testenv
```

Run tests:

```shell
$ make test
```

#### Docker

You need to have Docker installed in your development environment.

Docker image is used for both - running in production and on developers' machines as dependency (use `docker-compose`).
Here's how you can build docker image locally.

Run the build:

```shell
$ make docker-build
```

Restart containers:

```shell
$ make docker-down
$ make docker-up
```

Check docker logs:

```shell
$ make docker-logs
```

Log in to the bash on the service

```shell
$ make docker-bash
```
## Alembic work

Merge alembic migrations:


```shell

$ make alembic-merge-heads

```

Make migrations:

```shell

$ make migrations
```

Apply migrations:

```shell

$ make migrate
```


Check other useful commands in Makefile


# exo_formulaire

```
export COMPOSE_PROJECT_NAME=exo_formulaire
```

```
docker-compose up -d
```

to stop

```
docker-compose down"
```

to build but not run

```
docker-compose up --no-start
```

to run specific steps

```
docker-compose start sqlite3 create
```

```
docker-compose start insert
```

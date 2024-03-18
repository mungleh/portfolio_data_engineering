# Mini projet data ingenierie

### Déploiement d'une BDD sqlite avec un script de récupération de csv par HTML, un script d'injection des données avec manipulation SQL (création des tables, typage, etc...)

to start
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

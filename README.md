# PSA: [API RESTful Módulo de Soporte](https://psa-api-support.herokuapp.com/)

## Requisitos

- python3.6
- virtualenv
- Heroku CLI

---

## Instalación

```
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Salir de venv

```
deactivate
```

### Run local

```
python app.py
```

---

## Heroku

El comando `git remote -v` debería mostrar una salida parecida a la siguiente:

```
heroku	https://git.heroku.com/psa-api-support.git (fetch)
heroku	https://git.heroku.com/psa-api-support.git (push)
origin	git@github.com:eprediger/psa-support.git (fetch)
origin	git@github.com:eprediger/psa-support.git (push)
```

De lo contrario, vincular el repositorio ejecutando `heroku git:remote -a psa-api-support`

### Despliegue

```
git push heroku master
```


### Logs

```
heroku logs --tail
```

#### Base de Datos: `heroku pg:info`

### Scaling

```
heroku ps
heroku ps:scale web=0
heroku ps:scale web=1
```

### Run bdd tests

```
behave
```
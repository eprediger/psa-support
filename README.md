# PSA: [API RESTful Módulo de Soporte](https://blooming-badlands-85138.herokuapp.com/)

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

### Despliegue

```
git push heroku master
```

### Logs

```
heroku logs --tail
```

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
# FastApi, BD, testing

## Despligue en local

Despliegue en local usando BD sqlite local
```
export TESTING=True
echo $TESTING
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
uvicorn app.main:app 
```
Prueba de acceso
```
firefox http://localhost:8000/docs
```

### Pruebas en local

```
pytest tests/tests_main.py 
```

## Despliege con docker compose y BD externa

1. Desactivar variable de entorno TESTING
1. Revisar fichero de entorno `.env`
1. Se construye imagen de la aplicación
1. Se inicia BD
1. Se inicia adminer
1. Comprobar BD: Acceder a BD desde adminer
1. Se inicia aplicacíon

```
export TESTING=False
echo $TESTINg
cat .env
docker compose build
docker compose up -d bd
docker compose up -d adminer
firefox localhost:8080 &
docker compose up -d api
firefox localhost:8000/docs &
...

```
Terminar:
```
docker compose down --volumes 
```
### Pruebas en servidor

```
pytest tests/tests_server.py 

```
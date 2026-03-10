# PharmaManager — Backend

API Django REST Framework + PostgreSQL.

## Démarrage rapide

### Option Docker Compose (recommandée)

Depuis la racine du projet :

```bash
docker-compose up --build
```

- API : http://localhost:8000
- Swagger : http://localhost:8000/api/schema/swagger-ui/

### Option locale

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Documentation API : http://localhost:8000/api/schema/swagger-ui/

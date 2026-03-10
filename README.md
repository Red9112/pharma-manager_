# PharmaManager

Application de gestion de pharmacie — Développée dans le cadre du test technique SMARTHOLOL.

## Stack technique

- **Backend :** Django 4.x / 6.x, Django REST Framework, PostgreSQL, drf-spectacular (Swagger)
- **Frontend :** React.js (Vite), Axios, React Router
- **Documentation API :** Swagger (drf-spectacular)

## Prérequis

- Python 3.10+
- Node.js 18+
- PostgreSQL (ou Docker pour lancer une base locale)
- Optionnel : Docker pour PostgreSQL

### Lancer PostgreSQL avec Docker

```bash
docker run -d \
  --name pharma-postgres \
  -e POSTGRES_DB=pharma_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  -p 5432:5432 \
  postgres:16
```

Si le conteneur existait déjà avec un autre mot de passe, réinitialiser le mot de passe :

```bash
docker exec pharma-postgres psql -U postgres -d pharma_db -c "ALTER USER postgres PASSWORD 'postgres123';"
```

## Installation Backend

```bash
cd backend
python -m venv venv
# Windows :
venv\Scripts\activate
# Linux / Mac :
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos identifiants PostgreSQL si besoin

python manage.py migrate
python manage.py runserver
```

Le serveur API est disponible sur **http://localhost:8000**.

## Variables d'environnement (Backend)

Créer un fichier `backend/.env` à partir de `backend/.env.example` :

```
DEBUG=True
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=localhost 127.0.0.1

DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=127.0.0.1
DB_PORT=5432
```

## Installation Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Vérifier que VITE_API_BASE_URL pointe vers le backend (ex: http://localhost:8000/api/v1)

npm run dev
```

L'application est disponible sur **http://localhost:5173**.

## Variables d'environnement (Frontend)

Créer un fichier `frontend/.env` à partir de `frontend/.env.example` :

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Documentation API

Swagger UI : **http://localhost:8000/api/schema/swagger-ui/**

Schéma OpenAPI : **http://localhost:8000/api/schema/**

## Structure du projet

- `backend/` — Projet Django (config, apps medicaments, ventes, categories)
- `frontend/` — Application React (Vite), pages Dashboard, Médicaments, Ventes

## Livrables

- Backend : API REST (médicaments, catégories, ventes), Swagger, soft delete, alertes stock, annulation de vente avec réintégration du stock
- Frontend : Page Médicaments (liste, filtres, formulaire, alertes stock), Page Ventes (création, historique, annulation), Dashboard (compteurs, alertes, ventes du jour)

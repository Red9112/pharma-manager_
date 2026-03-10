# PharmaManager — Frontend

Application React (Vite) pour l’interface PharmaManager.

## Démarrage rapide

### Option Docker Compose (UI via Nginx)

Depuis la racine du projet :

```bash
docker-compose up --build
```

Interface : http://localhost:3000

### Option locale (Vite)

```bash
npm install
cp .env.example .env
npm run dev
```

Configurer `VITE_API_BASE_URL` dans `.env` (ex. `http://localhost:8000/api/v1`). Le backend doit être démarré pour que les données s’affichent.

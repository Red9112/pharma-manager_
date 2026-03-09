"""
Script de test de connexion PostgreSQL.
À lancer depuis backend/ : python test_db_connection.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.conf import settings
from django.db import connection

db = settings.DATABASES["default"]
print(f"Connexion à: host={db['HOST']}, port={db['PORT']}, db={db['NAME']}, user={db['USER']}")
print(f"Password: {len(db['PASSWORD'])} caractères, repr={repr(db['PASSWORD'])}")
if "DB_PASSWORD" in os.environ:
    print("ATTENTION: DB_PASSWORD est défini dans l'environnement (écrase .env)")

try:
    connection.ensure_connection()
    print("OK: Connexion réussie.")
except Exception as e:
    print(f"ERREUR: {e}")

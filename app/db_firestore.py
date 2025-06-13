# db_firestore.py

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Caminho do JSON seguro via .env
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Inicialização única do Firebase
def iniciar_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()

# Instância do Firestore que será importada pelos outros módulos
db = iniciar_firebase()

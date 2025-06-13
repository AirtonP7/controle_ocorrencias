# app/components/feedback_db.py

from app.db_firestore import db
from datetime import datetime

def salvar_feedback(nome, email, mensagem, tipo="Geral"):
    try:
        doc_ref = db.collection("feedbacks").document()
        doc_ref.set({
            "nome": nome,
            "email": email,
            "mensagem": mensagem,
            "tipo": tipo,
            "data_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True
    except Exception as e:
        print(f"Erro ao salvar feedback: {e}")
        return False

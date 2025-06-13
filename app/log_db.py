from app.db_firestore import db
from datetime import datetime
from app.temas import aplicar_tema


def registrar_log(usuario, perfil, acao, alvo, detalhes=""):
    aplicar_tema()
    db.collection("logs_auditoria").add({
        "usuario": usuario,
        "perfil": perfil,
        "acao": acao,
        "alvo": alvo,
        "detalhes": detalhes,
        "momento": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

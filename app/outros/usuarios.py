# usuarios.py

from db_firestore import db

def adicionar_usuario(cargo, login, nome_completo, perfil, senha, setor):
    doc_ref = db.collection("usuarios").document()
    doc_ref.set({
        "cargo": cargo,
        "login": login,
        "nome completo": nome_completo,
        "perfil": perfil,
        "senha": senha,
        "setor": setor
    })

def listar_usuarios():
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection("usuarios").stream()]

def atualizar_usuario(usuario_id, dados: dict):
    db.collection("usuarios").document(usuario_id).update(dados)

def excluir_usuario(usuario_id):
    db.collection("usuarios").document(usuario_id).delete()

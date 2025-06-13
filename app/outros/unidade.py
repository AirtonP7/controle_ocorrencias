# unidade.py

from db_firestore import db

def adicionar_unidade(cep, cnpj, nome, numero, rua):
    doc_ref = db.collection("unidade").document()
    doc_ref.set({
        "cep": cep,
        "cnpj": cnpj,
        "nome": nome,
        "numero": numero,
        "rua": rua
    })

def listar_unidades():
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection("unidade").stream()]

def atualizar_unidade(unidade_id, dados: dict):
    db.collection("unidade").document(unidade_id).update(dados)

def excluir_unidade(unidade_id):
    db.collection("unidade").document(unidade_id).delete()

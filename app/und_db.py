from app.db_firestore import db
import streamlit as st

def adicionar_unidade(nome, cnpj, rua, numero, cep):
    doc_ref = db.collection("unidades").document()
    doc_ref.set({
        "nome": nome,
        "cnpj": cnpj,
        "rua": rua,
        "numero": numero,
        "cep": cep
    })

@st.cache_data(ttl=60)
def listar_unidades():
    unidades = []
    docs = db.collection("unidades").get()
    for doc in docs:
        unidade = doc.to_dict()
        unidade["id"] = doc.id
        unidades.append(unidade)
    return unidades

def editar_unidade(id_unidade, novo_nome, novo_cnpj, nova_rua, novo_numero, novo_cep):
    db.collection("unidades").document(id_unidade).update({
        "nome": novo_nome,
        "cnpj": novo_cnpj,
        "rua": nova_rua,
        "numero": novo_numero,
        "cep": novo_cep
    })

def excluir_unidade(id_unidade):
    db.collection("unidades").document(id_unidade).delete()
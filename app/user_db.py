import streamlit as st
from app.db_firestore import db
from datetime import datetime
from app.log_db import registrar_log

def adicionar_usuario(login, nome, perfil, cargo, setor):
    """
    Adiciona um novo usuário na coleção 'usuarios' do Firestore.
    A senha é gerenciada pelo Firebase Authentication.
    """
    doc_ref = db.collection("usuarios").document()
    doc_ref.set({
        "login": login,
        "nome_completo": nome,
        "perfil": perfil,
        "cargo": cargo,
        "setor": setor
    })

    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Criação de usuário",
        alvo=f"Usuário: {login}",
        detalhes=f"Perfil: {perfil}, Nome: {nome}"
    )

@st.cache_data(ttl=60)
def listar_usuarios():
    usuarios = []
    docs = db.collection("usuarios").get()
    for doc in docs:
        usuario = doc.to_dict()
        usuario["id"] = doc.id
        usuarios.append(usuario)
    return usuarios

@st.cache_data(ttl=60)
def buscar_perfil_por_email(email):
    """
    Busca o perfil do usuário na coleção 'usuarios' com base no e-mail (campo login).
    """
    try:
        usuarios_ref = db.collection("usuarios")
        query = usuarios_ref.where("login", "==", email).limit(1)
        resultados = query.get()

        for doc in resultados:
            dados = doc.to_dict()
            return dados.get("perfil")
        
        return None
    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        return None

def editar_usuario(id_usuario, login, nome, perfil, cargo, setor):
    db.collection("usuarios").document(id_usuario).update({
        "login": login,
        "nome_completo": nome,
        "perfil": perfil,
        "cargo": cargo,
        "setor": setor
    })

    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Edição de usuário",
        alvo=f"Usuário ID: {id_usuario}",
        detalhes=f"Novo login: {login}, Perfil: {perfil}"
    )

def excluir_usuario(id_usuario):
    db.collection("usuarios").document(id_usuario).delete()
    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Exclusão de usuário",
        alvo=f"Usuário ID: {id_usuario}"
    )

@st.cache_data(ttl=60)
def buscar_nome_por_email(email):
    """
    Busca o nome completo do usuário na coleção 'usuarios' com base no e-mail (campo login).
    """
    try:
        usuarios_ref = db.collection("usuarios")
        query = usuarios_ref.where("login", "==", email).limit(1)
        resultados = query.get()

        for doc in resultados:
            dados = doc.to_dict()
            return dados.get("nome_completo")
        
        return email  # fallback: mostra o e-mail se não encontrar o nome
    except Exception as e:
        print(f"Erro ao buscar nome: {e}")
        return email

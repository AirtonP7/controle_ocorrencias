import streamlit as st
from app.user_db import validar_login

def login():
    st.title("Controle de Ocorrencias")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        dados_usuario = validar_login(usuario, senha)
        if dados_usuario:
            id_usuario, login_db, perfil = dados_usuario
            st.session_state.usuario = login_db
            st.session_state.perfil = perfil
            st.session_state.id_usuario = id_usuario
            st.success(f"Bem-vindo, {login_db}!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

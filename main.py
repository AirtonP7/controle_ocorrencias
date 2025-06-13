import streamlit as st

# Configuração da página Título e Ícone
st.set_page_config(
    page_title="Grupo Max | Controle de Ocorrencias", #🔹 Título da página (aparece na aba do navegador)
    page_icon="https://i.postimg.cc/Df5wFvD9/Design-sem-nome-2023-03-17-T165226-578.png", #🔹 Ícone da página (pode ser emoji ou URL de imagem)
    layout="centered",  # 🔹 Define o layout da página ("wide" p/Expandido ou "centered" p/ centralizado)
    initial_sidebar_state="expanded",  # 🔹 Estado inicial da barra lateral ("auto", "expanded", "collapsed")
    #menu_items={  # 🔹 Personaliza o menu superior do Streamlit
        #"Get Help": "https://docs.streamlit.io/",  # Link para ajuda
        #"Report a bug": "https://github.com/streamlit/streamlit/issues",  # Link para reportar bugs
        #"About": "Este é um app criado com Streamlit 🚀"  # Texto sobre o app
    #}
)

from app.login import render_app
from app.db_firestore import iniciar_firebase


def main():
    iniciar_firebase()

    # Verifica o estado de sessão e parâmetros da URL
    if 'usuario' in st.session_state:
        st.session_state.query_params = {'usuario': st.session_state.usuario}

    render_app()

if __name__ == "__main__":
    main()

import streamlit as st
from app.auth import login as login_func
from app.colaborador import painel_colaborador
from app.admin import painel_admin
from datetime import datetime, timedelta
from streamlit_cookies_manager import EncryptedCookieManager

# Inicialização do gerenciador de cookies com senha
cookies = EncryptedCookieManager(prefix="myapp_", password="BraSint7_c00k13_S3guRo")

# Garantir que os cookies estejam prontos antes de usar
if not cookies.ready():
    st.stop()

# Recuperar usuário a partir dos cookies ao iniciar
if "usuario" not in st.session_state:
    usuario = cookies.get("usuario")
    perfil = cookies.get("perfil")
    if usuario and perfil:
        st.session_state["usuario"] = usuario
        st.session_state["perfil"] = perfil
        st.session_state["logged_in"] = True

# Verificar a expiração da sessão
def verificar_expiracao_sessao():
    tempo_expiracao = timedelta(minutes=10080)
    agora = datetime.now()

    if "ultimo_acesso" in st.session_state:
        ultimo_acesso = st.session_state["ultimo_acesso"]
        if isinstance(ultimo_acesso, str):
            ultimo_acesso = datetime.strptime(ultimo_acesso, "%Y-%m-%d %H:%M:%S")

        if agora - ultimo_acesso > tempo_expiracao:
            st.warning("⏳ Sua sessão expirou por inatividade.")
            st.session_state.clear()
            cookies.clear()
            st.rerun()
        else:
            st.session_state["ultimo_acesso"] = agora.strftime("%Y-%m-%d %H:%M:%S")
    elif "usuario" in st.session_state:
        st.session_state["ultimo_acesso"] = agora.strftime("%Y-%m-%d %H:%M:%S")

# Interface principal
def render_app():
    verificar_expiracao_sessao()

    if "logged_in" not in st.session_state:
        #st.markdown("""
        #<div style='text-align: center;'>
            #<img src='https://i.postimg.cc/DZyc0Ym6/fone-de-ouvido-removebg-preview.png' alt='' width='20%'>
            #<p></p>
        #</div>
        #""", unsafe_allow_html=True)
        login_func()



    else:
        perfil = st.session_state.get("perfil")
        usuario = st.session_state.get("usuario")

        if perfil in ["admin", "superadmin"]:
            painel_admin(usuario)
        elif perfil == "colaborador":
            painel_colaborador(usuario)
        else:
            st.error("⚠️ Perfil de usuário inválido ou não autorizado.")

if __name__ == "__main__":
    render_app()

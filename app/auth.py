import streamlit as st
from datetime import datetime, timedelta
from app.firebase_config import auth
from app.user_db import buscar_perfil_por_email

DOMINIO_PADRAO = "@grupomax.com"

def login():
    imagem_fundo = "https://i.postimg.cc/2y82hKkv/high-angle-desktop-with-laptop-copy-space.jpg"
    cor_texto = "#FAF8F8"
    cor_caixa = "transparent"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{imagem_fundo}") no-repeat center center fixed;
            background-size: cover;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes slideInDown {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}

        .login-container {{
            display: flex;
            flex-direction: column;
            align-items: center; /* Centraliza horizontalmente */
            justify-content: center; /* Centraliza verticalmente */
            width: 90%;
            padding-top: 60px;
            animation: fadeIn 2s ease-in-out;
        }}

        .login-box {{
            background-color: {cor_caixa};
            padding: 40px;
            border-radius: 16px;
            text-align: center;
            width: 100%;
            max-width: 360px;
            animation: fadeInUp 1.2s ease-out;
        }}

        .login-box h1 {{
            font-family: 'Segoe UI', sans-serif;
            font-size: 32px;
            margin-bottom: 25px;
            color: {cor_texto};
            text-shadow: 1px 1px 2px rgba(255,255,255,0.6);
            white-space: nowrap; /* Impede a quebra de linha */
            text-align: center; /* Centraliza o texto */
            animation: slideInDown 1.2s ease-out;
        }}

        .logo-img {{
            width: 130px;
            margin-bottom: 10px;
            display: block; /* Garante que a imagem seja tratada como um bloco */
            margin: 0 auto;
            margin-left: 100px; /* Move a imagem 20px para a direita */
            animation: fadeIn 1.5s ease-out, pulse 3s infinite;
        }}

        .stTextInput > div > input,
        .stPasswordInput > div > input {{
            border-radius: 8px;
            padding: 10px;
            background-color: rgba(255,255,255,0.5);
            color: {cor_texto};
        }}

        .stTextInput label, .stPasswordInput label {{
            color: {cor_texto};
        }}

        .stButton > button {{
            width: 100%;
            border-radius: 8px;
            background-color: #3399ff;
            color: white;
            font-weight: bold;
            margin-top: 10px;
            padding: 0.6em;
            transition: transform 0.2s ease, background-color 0.3s;
        }}

        .stButton > button:hover {{
            background-color: #1976d2;
            transform: scale(1.03);
        }}

        .footer-box {{
            margin-top: 80px;
            background-color: rgba(255, 255, 255, 0.5);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            width: fit-content;
            backdrop-filter: blur(8px);
        }}

        .footer-box p {{
            margin: 4px;
            color: {cor_texto};
            font-size: 15px;
        }}
        </style>

        <div class="login-container">
            <div class="login-box">
                <img src="https://i.postimg.cc/DZyc0Ym6/fone-de-ouvido-removebg-preview.png" class="logo-img" />
                <h1 style="color: white;">Controle de Ocorrências</h1>
        """,
        unsafe_allow_html=True
    )

    if "tentativas_login" not in st.session_state:
        st.session_state.tentativas_login = 0
    if "bloqueado_ate" not in st.session_state:
        st.session_state.bloqueado_ate = None

    agora = datetime.now()

    if st.session_state.bloqueado_ate:
        if agora < st.session_state.bloqueado_ate:
            restante = st.session_state.bloqueado_ate - agora
            minutos_restantes = int(restante.total_seconds() // 60) + 1
            st.warning(f"🚫 Você excedeu o limite de tentativas. Tente novamente em {minutos_restantes} minuto(s).")
            st.markdown("</div></div>", unsafe_allow_html=True)
            return
        else:
            st.session_state.tentativas_login = 0
            st.session_state.bloqueado_ate = None

    with st.form("login_form"):
        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if username and senha:
                email = f"{username.lower()}{DOMINIO_PADRAO}"
                try:
                    user = auth.sign_in_with_email_and_password(email, senha)
                    perfil = buscar_perfil_por_email(email)
                    if perfil:
                        st.session_state.usuario = email
                        st.session_state.perfil = perfil
                        st.session_state.logged_in = True
                        st.session_state.idToken = user['idToken']
                        st.session_state.tentativas_login = 0
                        st.success(f"✅ Bem-vindo, {username}!")
                        st.rerun()
                    else:
                        st.error("⚠️ Usuário autenticado, mas não cadastrado no Firestore.")
                except Exception:
                    st.session_state.tentativas_login += 1
                    tentativas_restantes = 5 - st.session_state.tentativas_login
                    if st.session_state.tentativas_login >= 5:
                        st.session_state.bloqueado_ate = agora + timedelta(minutes=15)
                        st.error("🚫 Muitas tentativas incorretas. Você foi bloqueado por 15 minutos.")
                    else:
                        st.error(f"❌ Usuário ou senha inválidos. Tentativas restantes: {tentativas_restantes}")
            else:
                st.warning("Preencha todos os campos.")

    st.markdown("</div>", unsafe_allow_html=True)  # fecha .login-box

       # Rodapé elegante com destaque
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 80px; font-size: 18px; color: white;'>
            <p>v1.2.2</p>
            <p>Copyright © Airton Pereira 2025</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# app/components/contato_feedback.py
import streamlit as st
import os
from app.temas import aplicar_tema
from app.components.feedback_db import salvar_feedback
from app.components.email_utils import enviar_email_feedback

def limpar_campos_feedback():
    st.session_state["nome_feedback"] = ""
    st.session_state["tipo_feedback"] = ""
    st.session_state["mensagem_feedback"] = ""

def contato_feedback():
    textColor = aplicar_tema()

    # Inicializa campos ANTES da renderização dos widgets
    for campo in ["nome_feedback", "tipo_feedback", "mensagem_feedback"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    # === ESTILO SOCIAL ===
    st.markdown("""
        <style>
        .social-btn {
            display: inline-block;
            margin: 8px;
            padding: 12px 18px;
            border-radius: 10px;
            color: #FFFFFF;
            font-weight: bold;
            text-decoration: none;
            font-size: 15px;
            transition: 0.3s;
        }
        .social-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 8px rgba(0,0,0,0.3);
        }
        .whatsapp { background-color: #00B050; }
        .instagram { background-color: #E1306C; }
        .linkedin { background-color: #0077b5; }
        .email { background-color: #0072C6; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='text-align: center; margin-top: 0px;'>
            <h1 style='background-color: {textColor};
                        color: white;
                        padding: 12px 24px;
                        border-radius: 10px;
                        font-weight: bold;
                        font-size: 32px;'>💬 Contato com o Desenvolvedor</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <p style='color: {textColor};
                  font-size: 20px;
                  font-weight: normal;
                  text-align: center;
                  margin-top: 0px;'>Escolha uma rede para contato direto:</p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <a href='https://wa.me/5585985762890?text=Olá%2C%20estou%20precisando%20de%20suporte.' target='_blank'>
                <img src='https://i.postimg.cc/zG8GTmxR/zap.png' width='80' height='80' style='border-radius: 20%;'>
            </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <a href='https://www.instagram.com/airtinho7/' target='_blank'>
                <img src='https://i.postimg.cc/5Nc0NQvg/insta.png' width='80' height='80' style='border-radius: 50%;'>
            </a>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <a href='https://www.linkedin.com/in/airton-pereira-579162236/' target='_blank'>
                <img src='https://i.postimg.cc/8c2BsLD6/link-3d.png' width='80' height='80' style='border-radius: 50%;'>
            </a>
        """, unsafe_allow_html=True)
    #with col4:
        #st.markdown("""
            #<a href='mailto:airtonpereiradev@gmail.com' target='_blank'>
                #<img src='https://i.postimg.cc/13xJz15j/gmail-3d.png' width='80' height='80' style='border-radius: 20%;'>
            #</a>
        #""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📣 Envie um Feedback direto")

    # === Formulário de Feedback ===
    with st.form("form_feedback", clear_on_submit=True):
        st.text_input("Seu nome", key="nome_feedback")
        st.selectbox(
            "Tipo de mensagem",
            ["", "Sugestão", "Relatar Problema", "Elogio"],
            index=["", "Sugestão", "Relatar Problema", "Elogio"].index(st.session_state["tipo_feedback"]) if st.session_state["tipo_feedback"] else 0,
            key="tipo_feedback"
        )
        st.text_area("Mensagem", key="mensagem_feedback")
        enviar = st.form_submit_button("📨 Enviar Feedback")

    if enviar:
        nome = st.session_state["nome_feedback"]
        tipo = st.session_state["tipo_feedback"]
        mensagem = st.session_state["mensagem_feedback"]
        email_usuario = st.session_state.get("usuario", "Desconhecido")

        if tipo and mensagem:
            sucesso = salvar_feedback(
                nome or "Anônimo",
                email_usuario,
                mensagem,
                tipo
            )

            assunto = f"📣 Novo Feedback: {tipo}"
            corpo = f"""
Novo feedback enviado!

👤 Nome: {nome or 'Anônimo'}
📧 Email: {email_usuario}
📌 Tipo: {tipo}

📝 Mensagem:
{mensagem}
""".strip()

            email_enviado = enviar_email_feedback(
                destinatario="airtonpereiradev@gmail.com",
                assunto=assunto,
                corpo_mensagem=corpo
            )

            if sucesso and email_enviado:
                st.success("✅ Feedback enviado com sucesso!")
            elif sucesso:
                st.warning("✅ Feedback salvo, mas falha ao enviar e-mail.")
            else:
                st.error("❌ Erro ao enviar feedback.")
        else:
            st.warning("⚠️ Escolha o tipo e escreva sua mensagem.")

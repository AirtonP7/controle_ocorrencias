import streamlit as st
from firebase_admin import auth as admin_auth
from app.user_db import listar_usuarios
from app.log_db import registrar_log
from app.admin_tools import redefinir_senha_firebase

def tela_redefinir_senha():
    st.subheader("🔑 Redefinir Senha de Usuário")

    usuarios = listar_usuarios()
    if not usuarios:
        st.info("Nenhum usuário cadastrado.")
        return

    # Permitir que ADMIN veja apenas admin e colaborador (não superadmin)
    if st.session_state.perfil == "admin":
        usuarios = [u for u in usuarios if u["perfil"] != "superadmin"]

    usuarios_opcoes = {
        f"{u['login']} - {u['nome_completo']} ({u['perfil']})": u for u in usuarios
    }

    usuario_escolhido = st.selectbox("Selecione o usuário", [""] + list(usuarios_opcoes.keys()))

    if usuario_escolhido:
        usuario_dados = usuarios_opcoes[usuario_escolhido]
        email = usuario_dados['login']
        perfil_alvo = usuario_dados['perfil']

        nova_senha = st.text_input("Nova senha", type="password")
        confirmar = st.text_input("Confirmar nova senha", type="password")

        if st.button("Redefinir Senha"):
            if st.session_state.perfil == "admin" and perfil_alvo == "superadmin":
                st.error("❌ Você não tem permissão para alterar a senha de um SuperAdmin.")
                return

            if not nova_senha or not confirmar:
                st.warning("Preencha os dois campos.")
            elif nova_senha != confirmar:
                st.warning("As senhas não coincidem.")
            elif len(nova_senha) < 6:
                st.warning("A senha deve ter no mínimo 6 caracteres.")
            else:
                try:
                    usuario = admin_auth.get_user_by_email(email)
                    redefinir_senha_firebase(usuario.uid, nova_senha)

                    registrar_log(
                        usuario=st.session_state.usuario,
                        perfil=st.session_state.perfil,
                        acao="Redefinição de senha",
                        alvo=f"Usuário: {email}",
                        detalhes="Senha redefinida manualmente"
                    )

                    st.success("✅ Senha redefinida com sucesso.")
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

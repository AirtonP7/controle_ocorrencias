# app/admin_tools.py

import firebase_admin
from firebase_admin import credentials, auth

# Inicia o Firebase Admin apenas uma vez
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\TI-001555\Desktop\AIRTON CONTROLE\PROJETOS\controles\controle-ocorrencias-fe8c5-firebase-adminsdk-fbsvc-8dc10b532e.json")
    firebase_admin.initialize_app(cred)

def criar_usuario_firebase(email, senha):
    try:
        user = auth.create_user(email=email, password=senha)
        return f"✅ Usuário criado no Firebase com UID: {user.uid}"
    except Exception as e:
        return f"❌ Erro ao criar usuário no Firebase: {e}"

def redefinir_senha_firebase(uid, nova_senha):
    try:
        auth.update_user(uid, password=nova_senha)
        return "✅ Senha redefinida com sucesso."
    except Exception as e:
        return f"❌ Erro ao redefinir senha: {e}"

def excluir_usuario_firebase(uid):
    try:
        auth.delete_user(uid)
        return "✅ Usuário removido do Firebase Authentication."
    except Exception as e:
        return f"❌ Erro ao excluir usuário do Firebase: {e}"

# 📋 Sistema de Controle de Ocorrências - Grupo Max

Sistema web completo e responsivo para registro, monitoramento e gestão de ocorrências em unidades e filiais do Grupo Max.

Desenvolvido com foco em **colaboradores, técnicos e administradores**, este sistema permite controle total sobre os atendimentos, pendências, relatórios e performance da equipe.

---

## 🚀 Funcionalidades

- ✅ Login seguro com autenticação via Firebase
- 🧑‍💼 Perfis de acesso: **Colaborador**, **Admin** e **SuperAdmin**
- 📝 Registro e edição de ocorrências com histórico
- 📊 Dashboard interativo com gráficos (Plotly)
- 🔍 Filtros dinâmicos e relatórios exportáveis
- 💬 Seção de contato e envio de feedback via e-mail
- 🔐 Segurança com cookies criptografados
- 📅 Agenda futura de envio de relatórios automáticos
- 🔧 Painel administrativo completo com logs e gerenciamento de usuários

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia         | Uso                                     |
|--------------------|------------------------------------------|
| **Streamlit**      | Frontend e backend da aplicação          |
| **Firebase**       | Autenticação, Firestore e hospedagem     |
| **Plotly**         | Visualizações interativas                |
| **Pandas**         | Manipulação de dados                     |
| **Pyrebase**       | Integração com Firebase Auth             |
| **smtplib**        | Envio de e-mails via Gmail               |
| **dotenv**         | Gerenciamento de variáveis sensíveis     |
| **EncryptedCookieManager** | Sessão segura com cookies criptografados |

---

## 📦 Instalação Local

1. Clone o repositório
```bash
git clone https://github.com/seuusuario/controle-ocorrencias.git
cd controle-ocorrencias

2. Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências:
pip install -r requirements.txt

4. Crie o arquivo .env com suas configurações:
# Dados do Firebase Admin SDK
GOOGLE_APPLICATION_CREDENTIALS="seu_arquivo_do_firebase".json

# Dados de e-mail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ORIGEM=seuemail@gmail.com
SENHA_EMAIL=sua_senha_de_app

5. Execute o app:
streamlit run main.py



☁️ Deploy no Render
Suba este projeto em um repositório GitHub (privado ou público)

Crie uma conta em: https://render.com

Crie um novo Web Service conectado ao GitHub

Configure:

Start command: streamlit run main.py

Build command: pip install -r requirements.txt

Python environment: 3.11+

Adicione as variáveis do .env no painel de Environment Variables do Render

⚠️ Importante: NÃO suba o arquivo .env nem o JSON com as credenciais do Firebase no repositório. Use o painel de variáveis do Render para isso.


📮 Contato com o Desenvolvedor
👨🏾‍💻 Airton Pereira

📧 airtonpereiradev@gmail.com

📱 WhatsApp

📸 Instagram

💼 LinkedIn


📮 Contato com o Desenvolvedor
👨🏾‍💻 Airton Pereira

📧 airtonpereiradev@gmail.com

📱 WhatsApp

📸 Instagram

💼 LinkedIn


📜 Licença
Este projeto é de Total dominio do desenvolvedor. Não é autorizada a cópia, redistribuição ou uso comercial sem permissão expressa do desenvolvedor e tem todos os direitos reservados © Airton Pereira.






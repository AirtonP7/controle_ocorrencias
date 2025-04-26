
# 📋 Controle de Ocorrências | GRUPOMAX

Sistema de gerenciamento de ocorrências internas da empresa **GRUPOMAX**, desenvolvido com **Python** e **Streamlit**.

---

## 🚀 Funcionalidades

- ✅ Registro de ocorrências com responsável técnico.
- ✅ Dashboard administrativo com KPIs e gráficos dinâmicos.
- ✅ Gerenciamento de usuários, unidades e ocorrências.
- ✅ Controle de permissões (Administrador / Colaborador).
- ✅ Filtros avançados em relatórios (por Unidade, Solicitante, Técnico, Status, Data).
- ✅ Exportação de relatórios em formato **Excel (.xlsx)**.
- ✅ Indicadores de performance e análise de pendências.
- ✅ Interface moderna, responsiva e amigável.

---

## 📦 Estrutura do Projeto

```
controle_ocorrencias/
├── app/
│   ├── admin.py
│   ├── auth.py
│   ├── colaborador.py
│   ├── dashboard_admin.py
│   ├── db.py
│   ├── login.py
│   ├── oco_db.py
│   ├── und_db.py
│   └── user_db.py
├── controle_ocorrencias.db   # Banco de dados SQLite (pode ser zerado antes do deploy)
├── main.py                   # Arquivo principal de execução
├── requirements.txt          # Dependências do projeto
└── README.md                 # Instruções e documentação do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **Streamlit**
- **Pandas**
- **Altair**
- **Openpyxl**
- **SQLite3** (embutido no Python)
- **Bcrypt** (para segurança de senhas)

---

## 📥 Como Executar Localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/controle_ocorrencias.git
   cd controle_ocorrencias
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   streamlit run main.py
   ```

4. Acesse o app no navegador:
   ```
   http://localhost:8501
   ```

---

## ☁️ Publicação na Nuvem

Você pode facilmente publicar o sistema usando:

- [Streamlit Community Cloud](https://streamlit.io/cloud) (Grátis)
- Render.com
- Heroku
- Vercel

> Basta fazer o upload do projeto no GitHub e conectar à plataforma!

---

## 📧 Suporte Técnico

- 📱 WhatsApp: [85 98576-2890](https://wa.me/5585985762890)
- 📧 Email: [airtonpereiradev@gmail.com](mailto:airtonpereiradev@gmail.com)

---

## 🔖 Informações Adicionais

- Versão: **1.0.0**
- Desenvolvedor: **Airton Pereira**
- Copyright © **2025**

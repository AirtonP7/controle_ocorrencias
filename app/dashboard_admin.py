import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from app.oco_db import listar_ocorrencias
from app.temas import aplicar_tema

def painel_dashboard_admin():
    st.header("📊 Painel de Indicadores - Admin")
    aplicar_tema()

    tema = st.session_state.get("tema", "Claro")
    fundo_grafico = "#121212" if tema == "Escuro" else "#B2DFDB"
    cor_texto = "#E0E0E0" if tema == "Escuro" else "#000000"

    ocorrencias = listar_ocorrencias()
    if not ocorrencias:
        st.warning("Nenhuma ocorrência registrada.")
        return

    dados = []
    for o in ocorrencias:
        data = o['data_registro']
        dias = (date.today() - datetime.strptime(data, "%Y-%m-%d").date()).days if o['status_atividade'] == "Pendente" else 0
        dados.append({
            "Data": data,
            "Unidade": o['unidade_solicitante'],
            "Solicitante": o['usuario_solicitante'],
            "Descrição": o['descricao'],
            "Técnico": o['tecnico_responsavel'],
            "Status": o['status_atividade'],
            "Dias Pendentes": dias,
            "Observações": o['observacao'] or ""
        })

    df = pd.DataFrame(dados)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Dias Pendentes"] = pd.to_numeric(df["Dias Pendentes"], errors="coerce")

    criticas = df[(df["Status"] == "Pendente") & (df["Dias Pendentes"] > 7)]
    if not criticas.empty:
        st.warning(f"⚠️ {len(criticas)} ocorrência(s) estão pendentes há mais de 7 dias!")

    # 🗓️ Filtros por período e status
    st.markdown("### 🗓️ Filtros por Período e Status")
    col1, col2, col3 = st.columns(3)

    hoje = date.today()
    data_min, data_max = df["Data"].min().date(), df["Data"].max().date()

    data_inicial = col1.date_input("De", value=hoje, min_value=data_min, max_value=data_max)
    data_final = col2.date_input("Até", value=hoje, min_value=data_min, max_value=data_max)

    status_opcao = col3.radio("Status", ["Todos", "Pendente", "Resolvida"], horizontal=True)

    df_filtrado = df[
        (df["Data"].dt.date >= data_inicial) &
        (df["Data"].dt.date <= data_final)
    ]

    if status_opcao != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Status"] == status_opcao]

    if df_filtrado.empty:
        st.warning("Nenhuma ocorrência no período/status selecionado.")
        return

    # 📊 Métricas
    total = len(df_filtrado)
    pendentes = (df_filtrado["Status"] == "Pendente").sum()
    resolvidas = (df_filtrado["Status"] == "Resolvida").sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Ocorrências", total)
    col2.metric("🕓 Pendentes", pendentes)
    col3.metric("✅ Resolvidas", resolvidas)

    st.markdown("---")
    st.markdown("### 🧠 Visão Geral")

    # 📈 Gráfico de status (Pizza)
    col1, col2 = st.columns(2)
    with col1:
        status_count = df_filtrado["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Total"]
        fig = px.pie(status_count, values="Total", names="Status",
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     title="Distribuição de Status", hole=0.4)

        fig.update_traces(textinfo="value+percent", textposition="outside", textfont=dict(size=14, color=cor_texto))
        fig.update_layout(paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
                          font=dict(color=cor_texto), title_font=dict(color=cor_texto),
                          legend_font=dict(color=cor_texto), showlegend=True,
                          margin=dict(t=50, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    # 📊 Ocorrências por dia
    with col2:
        df_diario = df_filtrado.groupby(df_filtrado["Data"].dt.date).size().reset_index(name="Total")
        fig = px.bar(df_diario, x="Data", y="Total", title="Ocorrências por Dia", text="Total")
        fig.update_traces(textposition="outside", textfont=dict(size=12, color=cor_texto))
        fig.update_layout(
            paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
            font=dict(family="Arial", color=cor_texto),
            title_font=dict(family="Arial", color=cor_texto),
            xaxis=dict(showticklabels=True, tickfont=dict(color=cor_texto), showgrid=False, showline=True, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False),
            margin=dict(t=50, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)

    # 📈 Evolução por Status (Área)
    st.markdown("### 📈 Evolução por Status")
    df_area = df_filtrado.groupby([df_filtrado["Data"].dt.date, "Status"]).size().reset_index(name="Total")
    fig = px.area(df_area, x="Data", y="Total", color="Status", line_group="Status", title="Status ao longo do tempo")
    fig.update_layout(
        paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto), title_font=dict(color=cor_texto),
        legend_title_font=dict(color=cor_texto), legend_font=dict(color=cor_texto),
        xaxis=dict(color=cor_texto, title_font=dict(color=cor_texto), tickfont=dict(color=cor_texto), showgrid=False),
        yaxis=dict(color=cor_texto, title_font=dict(color=cor_texto), tickfont=dict(color=cor_texto), showgrid=True)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 👨‍🔧 Ocorrências por Técnico
    st.markdown("### 👨‍🔧 Ocorrências por Técnico")
    tecnico_count = df_filtrado["Técnico"].value_counts().reset_index()
    tecnico_count.columns = ["Técnico", "Total"]
    fig = px.bar(tecnico_count, x="Total", y="Técnico", orientation='h',
                 color="Técnico", title="Volume por Técnico", text="Total")
    fig.update_traces(textposition="outside", textfont=dict(size=12, color=cor_texto))
    fig.update_layout(
        paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto), title_font=dict(color=cor_texto),
        legend_font=dict(color=cor_texto), legend_title_font=dict(color=cor_texto),
        xaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False, title=""),
        yaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📊 NOVO GRÁFICO: Média de Chamados por Dia por Técnico
    st.markdown("### 📊 Média Diária de Chamados por Técnico")
    df_medias = df_filtrado.groupby(["Técnico", df_filtrado["Data"].dt.date]).size().reset_index(name="Chamados")
    media_por_tecnico = df_medias.groupby("Técnico")["Chamados"].mean().reset_index(name="Média por Dia")
    fig = px.bar(media_por_tecnico, x="Média por Dia", y="Técnico", orientation='h',
                 text="Média por Dia", title="Média de Chamados por Dia por Técnico")
    fig.update_traces(textposition="outside", textfont=dict(size=12, color=cor_texto))
    fig.update_layout(
        paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto), title_font=dict(color=cor_texto),
        xaxis=dict(showticklabels=True, showgrid=False),
        yaxis=dict(showticklabels=True, showgrid=False),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 🏢 Ocorrências por Unidade
    st.markdown("### 🏢 Ocorrências por Unidade")
    unidade_count = df_filtrado["Unidade"].value_counts().reset_index()
    unidade_count.columns = ["Unidade", "Total"]
    fig = px.bar(unidade_count, x="Unidade", y="Total", color="Unidade",
                 title="Ocorrências por Loja", text="Total")
    fig.update_traces(textposition="outside", textfont=dict(size=12, color=cor_texto))
    fig.update_layout(
        paper_bgcolor=fundo_grafico, plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto), title_font=dict(color=cor_texto),
        legend_font=dict(color=cor_texto), legend_title_font=dict(color=cor_texto),
        xaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False, title=""),
        yaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 🔎 Pendências Críticas
    st.markdown("### 🔎 Ocorrências Pendentes Críticas")
    if not criticas.empty:
        st.dataframe(criticas[["Data", "Unidade", "Técnico", "Dias Pendentes", "Descrição"]], use_container_width=True)
    else:
        st.info("Sem pendências críticas no período.")

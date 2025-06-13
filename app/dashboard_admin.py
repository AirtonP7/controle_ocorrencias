# app/dashboard_admin.py
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

    criticas = df[(df["Status"] == "Pendente") & (df["Dias Pendentes"] > 2)]
    if not criticas.empty:
        st.warning(f"⚠️ {len(criticas)} ocorrência(s) estão pendentes há mais de 2 dias!")

    st.markdown("### 🗓️ Filtros por Período")
    col1, col2 = st.columns(2)
    data_min, data_max = df["Data"].min().date(), df["Data"].max().date()
    data_inicial = col1.date_input("De", value=data_min, min_value=data_min, max_value=data_max)
    data_final = col2.date_input("Até", value=data_max, min_value=data_min, max_value=data_max)

    df_filtrado = df[(df["Data"].dt.date >= data_inicial) & (df["Data"].dt.date <= data_final)]
    if df_filtrado.empty:
        st.warning("Nenhuma ocorrência no período selecionado.")
        return

    total = len(df_filtrado)
    pendentes = (df_filtrado["Status"] == "Pendente").sum()
    resolvidas = (df_filtrado["Status"] == "Resolvida").sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Ocorrências", total)
    col2.metric("🕓 Pendentes", pendentes)
    col3.metric("✅ Resolvidas", resolvidas)

    st.markdown("---")
    st.markdown("### 🧠 Visão Geral")

    col1, col2 = st.columns(2)

    with col1:
        status_count = df_filtrado["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Total"]
        fig = px.pie(
            status_count, 
            values="Total", 
            names="Status",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Distribuição de Status",
            hole=0.4
        )

        fig.update_traces(
            textinfo="value+percent",
            textposition="outside",  # Posiciona os rótulos fora do gráfico
            textfont=dict(size=14, color=cor_texto),
            marker=dict(line=dict(color=cor_texto, width=1))

        )

        fig.update_layout(
            paper_bgcolor=fundo_grafico,
            plot_bgcolor=fundo_grafico,
            font=dict(color=cor_texto),
            title_font=dict(color=cor_texto),
            legend_font=dict(color=cor_texto),
            showlegend=True,
            margin=dict(t=50, b=10, l=10, r=10)  # Ajuste de margens para evitar cortes
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_diario = df_filtrado.groupby(df_filtrado["Data"].dt.date).size().reset_index(name="Total")
        fig = px.bar(df_diario, x="Data", y="Total", title="Ocorrências por Dia", text="Total")

        fig.update_traces(textposition="outside", textfont=dict(size=12, color=cor_texto))

        fig.update_layout(
            paper_bgcolor=fundo_grafico,
            plot_bgcolor=fundo_grafico,
            font=dict(family="Arial", color=cor_texto),  # Define a fonte global
            title_font=dict(family="Arial", color=cor_texto),
            xaxis=dict(
                showticklabels=True,  # Exibe os rótulos do eixo X
                tickfont=dict(color=cor_texto),  # Ajusta a cor da fonte dos rótulos
                showgrid=False,
                showline=True,  # Adiciona uma linha para melhor visualização
                zeroline=False
            ),
            yaxis=dict(
                showticklabels=False,  # Remove os rótulos do eixo Y
                showgrid=False,
                showline=False,
                zeroline=False
            ),
            margin=dict(t=50, b=50)  # Ajusta a margem superior e inferior
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Evolução por Status")
    df_area = df_filtrado.groupby([df_filtrado["Data"].dt.date, "Status"]).size().reset_index(name="Total")
    fig = px.area(df_area, x="Data", y="Total", color="Status", line_group="Status", title="Status ao longo do tempo")
    fig.update_layout(
        paper_bgcolor=fundo_grafico,
        plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto),
        title_font=dict(color=cor_texto),
        legend_title_font=dict(color=cor_texto),
        legend_font=dict(color=cor_texto),
        xaxis=dict(color=cor_texto, title_font=dict(color=cor_texto), tickfont=dict(color=cor_texto), showgrid=False),
        yaxis=dict(color=cor_texto, title_font=dict(color=cor_texto), tickfont=dict(color=cor_texto), showgrid=True)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 👨‍🔧 Ocorrências por Técnico")
    tecnico_count = df_filtrado["Técnico"].value_counts().reset_index()
    tecnico_count.columns = ["Técnico", "Total"]
    fig = px.bar(
            tecnico_count, 
            x="Total", 
            y="Técnico", 
            orientation='h', 
            color="Técnico", 
            title="Volume por Técnico", 
            text="Total"
        )

    fig.update_traces(
            textposition="outside", 
            textfont=dict(size=12, color=cor_texto)
        )

    fig.update_layout(
            paper_bgcolor=fundo_grafico,
            plot_bgcolor=fundo_grafico,
            font=dict(color=cor_texto),
            title_font=dict(color=cor_texto),
            legend_font=dict(color=cor_texto),
            legend_title_font=dict(color=cor_texto),  # Ajusta a cor do título da legenda
            xaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False, title=""),
            yaxis=dict(showticklabels=False, showgrid=False, showline=False, zeroline=False),
            margin=dict(l=20, r=20, t=50, b=20)
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏢 Ocorrências por Unidade")
    unidade_count = df_filtrado["Unidade"].value_counts().reset_index()
    unidade_count.columns = ["Unidade", "Total"]
    fig = px.bar(
        unidade_count, 
        x="Unidade", 
        y="Total", 
        color="Unidade", 
        title="Ocorrências por Loja", 
        text="Total"
    )

    fig.update_traces(
        textposition="outside", 
        textfont=dict(size=12, color=cor_texto)
    )

    fig.update_layout(
        paper_bgcolor=fundo_grafico,
        plot_bgcolor=fundo_grafico,
        font=dict(color=cor_texto),
        title_font=dict(color=cor_texto),
        legend_font=dict(color=cor_texto),
        legend_title_font=dict(color=cor_texto),  # Ajusta a cor do título da legenda
        xaxis=dict(
            showticklabels=False, 
            showgrid=False, 
            showline=False, 
            zeroline=False,
            title=""  # Remove o título do eixo X
        ),
        yaxis=dict(
            showticklabels=False, 
            showgrid=False, 
            showline=False, 
            zeroline=False
        ),
        margin=dict(t=50, b=50, l=50, r=50)  # Ajuste de margens para evitar cortes
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔎 Ocorrências Pendentes Críticas")
    if not criticas.empty:
        st.dataframe(
            criticas[["Data", "Unidade", "Técnico", "Dias Pendentes", "Descrição"]],
            use_container_width=True
        )
    else:
        st.info("Sem pendências críticas no período.")

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.lancamento_controller import LancamentoController

def exibir_tela_dashboard():
    st.title("Resumo Financeiro")
    
    l_controller = LancamentoController()
    dados = l_controller.listar_todos()

    if not dados:
        st.info("Ainda não há dados suficientes para gerar o resumo. Realize alguns lançamentos primeiro.")
        return

    # 1. Preparação dos Dados
    df = pd.DataFrame([
        {
            "Data": pd.to_datetime(h.data_vencimento),
            "Valor": float(h.valor_bruto),
            "Status": h.status
        } for h in dados
    ])

    # 2. Seção de Cards (Métricas)
    col1, col2, col3, col4 = st.columns(4)
    
    total_geral = df["Valor"].sum()
    pago = df[df["Status"] == "Pago"]["Valor"].sum()
    pendente = df[df["Status"] == "Pendente"]["Valor"].sum()
    ticket_medio = df["Valor"].mean()

    col1.metric("Total Lançado", f"R$ {total_geral:,.2f}")
    col2.metric("Total Pago", f"R$ {pago:,.2f}")
    col3.metric("A Pagar", f"R$ {pendente:,.2f}", delta_color="inverse")
    col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.markdown("---")

    # 3. Gráficos
    col_esq, col_dir = st.columns([2, 1])

    with col_esq:
        st.subheader("Evolução de Vencimentos")
        df_timeline = df.groupby("Data")["Valor"].sum().reset_index()
        fig_line = px.line(df_timeline, x="Data", y="Valor", markers=True, template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_dir:
        st.subheader("Status")
        fig_pie = px.pie(df, values="Valor", names="Status", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
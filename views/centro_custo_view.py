import streamlit as st
import pandas as pd
from controllers.centro_custo_controller import CentroCustoController

def exibir_tela_centro_custo():
    st.title("Gestão de Centros de Custo")
    cc_controller = CentroCustoController()
    tab_lista, tab_novo = st.tabs(["Visualizar Centros", "Cadastrar Novo"])
    with tab_novo:
        with st.form("form_cc", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome_cc = col1.text_input("Nome do Centro de Custo")
            cod_cc = col2.text_input("Código Contábil")
            desc_cc = st.text_area("Descrição Detalhada")
            if st.form_submit_button("Salvar"):
                if cc_controller.criar(nome_cc, desc_cc, cod_cc):
                    st.success("Cadastrado!")
                    st.rerun()
    with tab_lista:
        centros = cc_controller.listar_todos()
        if centros:
            df = pd.DataFrame([{"ID": c.id, "Centro": c.centro_custo, "Código": c.codigo} for c in centros])
            st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd
from controllers.conta_bancaria_controller import ContaBancariaController

def exibir_tela_contas():
    st.title("Gestão de Contas Bancárias")
    cb_controller = ContaBancariaController()
    tab_lista, tab_novo = st.tabs(["Listar Contas", "Cadastrar Conta"])
    with tab_novo:
        with st.form("form_cb", clear_on_submit=True):
            col1, col2 = st.columns(2)
            cod = col1.text_input("Código")
            ag  = col2.text_input("Agência")
            num = col2.text_input("Número")
            tipo = st.selectbox("Tipo", ["Corrente", "Poupança", "Investimento", "Caixa Interno"])
            if st.form_submit_button("Salvar"):
                if cb_controller.criar(cod, ag, num, tipo):
                    st.success("Conta salva!")
                    st.rerun()
    with tab_lista:
        contas = cb_controller.listar_todos()
        if contas:
            df = pd.DataFrame([{"ID": c.id, "Código": c.codigo, "Agência": c.agencia, "Número": c.numero, "Tipo": c.tipo} for c in contas])
            st.dataframe(df, use_container_width=True)
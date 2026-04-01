import streamlit as st
import pandas as pd
from controllers.pessoa_controller import PessoaController

def exibir_tela_pessoas():
    st.title("Gestão de Pessoas")
    p_controller = PessoaController()
    tab_lista, tab_novo = st.tabs(["Listar Registros", "Novo Cadastro"])
    with tab_novo:
        with st.form("form_pessoa", clear_on_submit=True):
            nome = st.text_input("Nome ou Razão Social")
            cpf_cnpj = st.text_input("CPF ou CNPJ")
            if st.form_submit_button("Salvar"):
                if p_controller.criar(nome, cpf_cnpj):
                    st.success("Salvo com sucesso!")
                    st.rerun()
    with tab_lista:
        dados = p_controller.listar_todos()
        if dados:
            df = pd.DataFrame([{"ID": p.id, "Nome": p.nome_razao_social, "Documento": p.cpf_cnpj} for p in dados])
            st.dataframe(df, use_container_width=True, hide_index=True)
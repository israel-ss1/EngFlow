import streamlit as st
import pandas as pd
from controllers.plano_contas_controller import PlanoContasController

def exibir_tela_plano_contas():
    st.title("Estrutura do Plano de Contas")
    pc_controller = PlanoContasController()
    tab_hierarquia, tab_novo = st.tabs(["Visualizar", "Cadastrar"])
    with tab_novo:
        with st.form("form_pc", clear_on_submit=True):
            codigo = st.text_input("Código Contábil")
            nome_plano = st.text_input("Nome da Conta", max_chars=20)
            contas_existentes = pc_controller.listar_todos()
            opcoes_pai = {0: "Nenhum (Raiz)"}
            for c in contas_existentes: opcoes_pai[c.id] = f"{c.codigo_contabil} - {c.nome}"
            id_pai = st.selectbox("Conta Pai", options=list(opcoes_pai.keys()), format_func=lambda x: opcoes_pai[x])
            natureza = st.selectbox("Natureza", ["Ativo", "Passivo", "Patrimônio Líquido", "Receita", "Despesa"])
            if st.form_submit_button("Salvar"):
                if pc_controller.criar(id_pai, codigo, nome_plano, "", natureza):
                    st.success("Plano atualizado!")
                    st.rerun()
    with tab_hierarquia:
        planos = pc_controller.listar_todos()
        if planos:
            df = pd.DataFrame([{"Código": p.codigo_contabil, "Nome": p.nome, "Natureza": p.natureza} for p in planos])
            st.dataframe(df, use_container_width=True)
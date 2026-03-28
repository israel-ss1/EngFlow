# -*- coding: latin-1 -*-
import streamlit as st
import pandas as pd
from controllers.centro_custo_controller import CentroCustoController
from controllers.conta_bancaria_controller import ContaBancariaController
from controllers.plano_contas_controller import PlanoContasController

# Configuracao da pagina
st.set_page_config(page_title="EngFlow - Cadastro", layout="wide")

def main():
    st.sidebar.title("EngFlow v1.0")
    st.sidebar.markdown("---")
    
    # Instancia apenas o controller do Centro de Custo
    cc_controller = CentroCustoController()

    # Menu simplificado
    menu = ["Centro de Custo", "Contas Bancarias", "Plano de Contas", "Configuracoes"]
    choice = st.sidebar.selectbox("Menu Principal", menu)

    # --- TELA: CENTRO DE CUSTO ---
    if choice == "Centro de Custo":
        st.title("Gestao de Centros de Custo")
        
        tab_lista, tab_novo = st.tabs(["Visualizar Centros", "Cadastrar Novo"])
        
        with tab_novo:
            st.subheader("Novo Registro")
            with st.form("form_cc", clear_on_submit=True):
                col1, col2 = st.columns(2)
                nome_cc = col1.text_input("Nome do Centro de Custo")
                cod_cc = col2.text_input("Codigo Contabil")
                desc_cc = st.text_area("Descricao Detalhada")
                
                if st.form_submit_button("Salvar"):
                    if nome_cc and cod_cc:
                        sucesso = cc_controller.criar(nome_cc, desc_cc, cod_cc)
                        if sucesso:
                            st.success(f"Centro '{nome_cc}' cadastrado!")
                            st.rerun()
                        else:
                            st.error("Erro ao salvar no banco. Verifique o terminal.")
                    else:
                        st.warning("Por favor, preencha Nome e Codigo.")

        with tab_lista:
            st.subheader("Listagem Atual")
            centros = cc_controller.listar_todos()
            
            if centros:
                # Transformamos os objetos do SQLAlchemy em lista para o DataFrame
                df_cc = pd.DataFrame([
                    {"ID": c.id, "Centro": c.centro_custo, "Codigo": c.codigo, "Descricao": c.descricao} 
                    for c in centros
                ])
                st.dataframe(df_cc, use_container_width=True)
                
                st.markdown("---")
                # Area de exclusao
                with st.expander("Remover Centro de Custo"):
                    id_remover = st.number_input("Digite o ID para excluir", min_value=1, step=1)
                    if st.button("Confirmar Exclusao", type="secondary"):
                        if cc_controller.deletar(id_remover):
                            st.success(f"ID {id_remover} removido.")
                            st.rerun()
                        else:
                            st.error("Nao foi possivel remover. ID inexistente?")
            else:
                st.info("Nenhum Centro de Custo cadastrado ainda.")

    # --- TELA: CONFIGURACOES ---
    elif choice == "Configuracoes":
        st.title("Configuracoes")
        st.write("Conectado como: **sa**")
        st.write("Servidor: **DESKTOP-LO3B79V**")
        st.write("Banco: **EngFlow**")
        
    # --- TELA: CONTAS BANCARIAS ---
    elif choice == "Contas Bancarias":
        st.title("Gestao de Contas Bancarias")
        cb_controller = ContaBancariaController()
    
        tab_lista, tab_novo = st.tabs(["Listar Contas", "Cadastrar Conta"])
    
        with tab_novo:
            with st.form("form_cb", clear_on_submit=True):
                col1, col2 = st.columns(2)
                cod = col1.text_input("Codigo da Conta (ex: 001)")
                num = col2.text_input("Numero da Conta")
                tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupanca", "Investimento", "Caixa Interno"])
            
                if st.form_submit_button("Salvar Conta"):
                    if cod and num:
                        if cb_controller.criar(cod, num, tipo_conta):
                            st.success("Conta cadastrada!")
                            st.rerun()
                    else:
                        st.error("Codigo e Numero sao obrigatorios.")

        with tab_lista:
            contas = cb_controller.listar_todos()
            if contas:
                df_cb = pd.DataFrame([
                    {"ID": c.id, "Codigo": c.codigo, "Numero": c.numero, "Tipo": c.tipo} 
                    for c in contas
                ])
                st.dataframe(df_cb, use_container_width=True)
                
    # --- TELA: PLANO DE CONTAS ---
    elif choice == "Plano de Contas":
        st.title("Estrutura do Plano de Contas")
        pc_controller = PlanoContasController()
    
        tab_hierarquia, tab_novo = st.tabs(["Visualizar Estrutura", "Cadastrar Nova Conta"])
    
        with tab_novo:
            st.subheader("Cadastro de Conta Contabil")
            with st.form("form_pc", clear_on_submit=True):
                col1, col2 = st.columns(2)
                # O ID foi removido pois o SQL Server gera automaticamente (IDENTITY)
                codigo = col1.text_input("Codigo Contabil (Ex: 1.1.01)")
                nome_plano = col2.text_input("Nome da Conta (Max 20 carac.)", max_chars=20)
            
                # Carrega contas existentes para popular o select de 'Conta Pai'
                contas_existentes = pc_controller.listar_todos()
                opcoes_pai = {0: "Nenhum (Nivel Superior / Raiz)"}
                for c in contas_existentes:
                    opcoes_pai[c.id] = f"{c.codigo_contabil} - {c.nome}"
            
                id_pai = st.selectbox(
                    "Vincular a Conta Pai:", 
                    options=list(opcoes_pai.keys()), 
                    format_func=lambda x: opcoes_pai[x]
                )
            
                desc = st.text_area("Descricao Completa / Observacoes")
                natureza = st.selectbox("Natureza da Conta", ["Ativo", "Passivo", "Patrimonio Liquido", "Receita", "Despesa"])
            
                if st.form_submit_button("Salvar no Plano de Contas"):
                    if codigo and nome_plano:
                        sucesso = pc_controller.criar(id_pai, codigo, nome_plano, desc, natureza)
                        if sucesso:
                            st.success(f"Conta '{nome_plano}' cadastrada com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao salvar. Verifique se o Codigo Contabil ja existe ou se ha erro de conexao.")
                    else:
                        st.warning("Codigo e Nome sao campos obrigatorios.")

        with tab_hierarquia:
            st.subheader("Hierarquia Atual")
            dados = pc_controller.listar_todos()
        
            if dados:
                lista_para_tabela = []
                for d in dados:
                    # Logica visual para indentar filhos baseado nos pontos do codigo (ex: 1.1.01)
                    nivel = d.codigo_contabil.count('.')
                    indentacao = " " * (nivel * 6) # Espacamento visual
                
                    lista_para_tabela.append({
                        "Codigo": d.codigo_contabil,
                        "Nome da Conta": indentacao + d.nome,
                        "Natureza": d.natureza,
                        "Descricao": d.descricao
                    })
            
                st.table(lista_para_tabela)
            else:
                st.info("O Plano de Contas esta vazio. Comece cadastrando as contas de nivel superior.")

if __name__ == "__main__":
    main()
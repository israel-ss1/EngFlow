# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime

# Importação dos Controllers
from controllers.centro_custo_controller import CentroCustoController
from controllers.conta_bancaria_controller import ContaBancariaController
from controllers.plano_contas_controller import PlanoContasController
from controllers.pessoa_controller import PessoaController
from controllers.usuario_controller import UsuarioController
from controllers.lancamento_controller import LancamentoController

# Configuracao da pagina
st.set_page_config(page_title="EngFlow - Gestao Financeira", layout="wide")

# ==========================================
# FUNÇÕES DE INTERFACE (VIEWS)
# ==========================================

def exibir_tela_lancamentos():
    st.title("Gestao de Lancamentos Financeiros")
    
    l_controller = LancamentoController()
    p_controller = PessoaController()
    cb_controller = ContaBancariaController()
    pc_controller = PlanoContasController()
    cc_controller = CentroCustoController()

    tab_lista, tab_novo = st.tabs(["Listar Lancamentos", "Novo Lancamento (Mestre/Detalhe)"])

    with tab_novo:
        st.subheader("1. Dados Principais (Mestre)")
        
        lista_pessoas = p_controller.listar_todos()
        lista_contas = cb_controller.listar_todos()
        lista_planos = pc_controller.listar_todos()
        lista_centros = cc_controller.listar_todos()

        with st.form("form_lancamento"):
            col1, col2, col3 = st.columns(3)
            pessoa_sel = col1.selectbox("Pessoa/Empresa", options=lista_pessoas, format_func=lambda x: x.nome_razao_social)
            conta_sel = col2.selectbox("Conta Bancaria", options=lista_contas, format_func=lambda x: f"{x.codigo} - {x.numero}")
            tipo_doc = col3.selectbox("Tipo Documento", ["Boleto", "Nota Fiscal", "Recibo", "Transferencia", "Pix"])

            col4, col5, col6 = st.columns(3)
            data_venc = col4.date_input("Data Vencimento", value=datetime.now())
            data_comp = col5.date_input("Data Competencia", value=datetime.now())
            data_liq = col6.date_input("Data Liquidacao (Opcional)", value=None)

            col7, col8, col9 = st.columns(3)
            vlr_bruto = col7.number_input("Valor Bruto", min_value=0.0, step=0.01, format="%.2f")
            vlr_liquido = col8.number_input("Valor Liquido", min_value=0.0, step=0.01, format="%.2f")
            status_sel = col9.selectbox("Status", ["Pendente", "Pago", "Agendado", "Cancelado"])

            st.markdown("---")
            st.subheader("2. Rateio (Detalhes)")
            st.info("Distribua o valor total entre o Plano de Contas e Centros de Custo.")

            df_rateio_input = pd.DataFrame([
                {"Plano de Contas": "", "Centro de Custo": "", "Valor Parcela": 0.0, "Observacao": ""}
            ])

            config_colunas = {
                "Plano de Contas": st.column_config.SelectboxColumn(options=[f"{p.codigo_contabil} - {p.nome}" for p in lista_planos], required=True),
                "Centro de Custo": st.column_config.SelectboxColumn(options=[c.centro_custo for c in lista_centros], required=True),
                "Valor Parcela": st.column_config.NumberColumn(format="R$ %.2f", min_value=0, required=True),
                "Observacao": st.column_config.TextColumn()
            }
            
            edicao_rateio = st.data_editor(
                df_rateio_input, 
                num_rows="dynamic", 
                column_config=config_colunas,
                use_container_width=True,
                key="editor_rateio"
            )

            btn_salvar = st.form_submit_button("Confirmar Lancamento Completo")

            if btn_salvar:
                total_rateio = sum(item['Valor Parcela'] for item in edicao_rateio)
                
                if total_rateio != vlr_bruto:
                    st.error(f"Erro: Soma do rateio (R$ {total_rateio:.2f}) difere do Valor Bruto (R$ {vlr_bruto:.2f})")
                elif not pessoa_sel or not conta_sel:
                    st.warning("Selecione a Pessoa e a Conta Bancaria.")
                else:
                    dados_mestre = {
                        "id_pessoa": pessoa_sel.id,
                        "id_conta_bancaria": conta_sel.id,
                        "data_vencimento": data_venc,
                        "data_competencia": data_comp,
                        "data_liquidacao": data_liq,
                        "valor_bruto": vlr_bruto,
                        "valor_liquido": vlr_liquido,
                        "status": status_sel,
                        "tipo_documento": tipo_doc,
                        "criado_por": 1, 
                        "criado_em": datetime.now()
                    }

                    lista_final_rateio = []
                    try:
                        for row in edicao_rateio:
                            p_cod = row['Plano de Contas'].split(" - ")[0]
                            id_pc = next(p.id for p in lista_planos if p.codigo_contabil == p_cod)
                            id_cc = next(c.id for c in lista_centros if c.centro_custo == row['Centro de Custo'])

                            lista_final_rateio.append({
                                "id_plano_contas": id_pc,
                                "id_centro_custo": id_cc,
                                "valor_parcela": row['Valor Parcela'],
                                "observacao": row['Observacao']
                            })

                        if l_controller.salvar_completo(dados_mestre, lista_final_rateio):
                            st.success("Lancamento e Rateio salvos com sucesso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao processar dados: {e}")

    with tab_lista:
        st.subheader("Historico de Lancamentos")
        historico = l_controller.listar_todos()
        if historico:
            df_hist = pd.DataFrame([
                {
                    "Vencimento": h.data_vencimento,
                    "Valor Bruto": h.valor_bruto,
                    "Status": h.status,
                    "Doc": h.tipo_documento
                } for h in historico
            ])
            st.dataframe(df_hist, use_container_width=True)
        else:
            st.info("Nenhum lancamento encontrado.")

def exibir_tela_centro_custo():
    st.title("Gestao de Centros de Custo")
    cc_controller = CentroCustoController()
    tab_lista, tab_novo = st.tabs(["Visualizar Centros", "Cadastrar Novo"])
    with tab_novo:
        with st.form("form_cc", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome_cc = col1.text_input("Nome do Centro de Custo")
            cod_cc = col2.text_input("Codigo Contabil")
            desc_cc = st.text_area("Descricao Detalhada")
            if st.form_submit_button("Salvar"):
                if cc_controller.criar(nome_cc, desc_cc, cod_cc):
                    st.success("Cadastrado!")
                    st.rerun()
    with tab_lista:
        centros = cc_controller.listar_todos()
        if centros:
            df = pd.DataFrame([{"ID": c.id, "Centro": c.centro_custo, "Codigo": c.codigo} for c in centros])
            st.dataframe(df, use_container_width=True)

def exibir_tela_pessoas():
    st.title("Gestao de Pessoas")
    p_controller = PessoaController()
    tab_lista, tab_novo = st.tabs(["Listar Registros", "Novo Cadastro"])
    with tab_novo:
        with st.form("form_pessoa", clear_on_submit=True):
            nome = st.text_input("Nome ou Razao Social")
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

def exibir_tela_usuarios():
    st.title("Gestao de Usuarios")
    u_controller = UsuarioController()
    tab_lista, tab_novo = st.tabs(["Listar Usuarios", "Novo Usuario"])
    with tab_novo:
        with st.form("form_usuario", clear_on_submit=True):
            nome_u = st.text_input("Nome Completo")
            email_u = st.text_input("E-mail")
            senha_u = st.text_input("Senha", type="password")
            papel_u = st.selectbox("Perfil", ["Administrador", "Gerente", "Operador", "Leitura"])
            if st.form_submit_button("Cadastrar"):
                if u_controller.criar(nome_u, email_u, senha_u, papel_u):
                    st.success("Usuario criado!")
                    st.rerun()

def exibir_tela_contas():
    st.title("Gestao de Contas Bancarias")
    cb_controller = ContaBancariaController()
    tab_lista, tab_novo = st.tabs(["Listar Contas", "Cadastrar Conta"])
    with tab_novo:
        with st.form("form_cb", clear_on_submit=True):
            col1, col2 = st.columns(2)
            cod = col1.text_input("Codigo")
            num = col2.text_input("Numero")
            tipo = st.selectbox("Tipo", ["Corrente", "Poupanca", "Investimento", "Caixa Interno"])
            if st.form_submit_button("Salvar"):
                if cb_controller.criar(cod, num, tipo):
                    st.success("Conta salva!")
                    st.rerun()

def exibir_tela_plano_contas():
    st.title("Estrutura do Plano de Contas")
    pc_controller = PlanoContasController()
    tab_hierarquia, tab_novo = st.tabs(["Visualizar", "Cadastrar"])
    with tab_novo:
        with st.form("form_pc", clear_on_submit=True):
            codigo = st.text_input("Codigo Contabil")
            nome_plano = st.text_input("Nome da Conta", max_chars=20)
            contas_existentes = pc_controller.listar_todos()
            opcoes_pai = {0: "Nenhum (Raiz)"}
            for c in contas_existentes: opcoes_pai[c.id] = f"{c.codigo_contabil} - {c.nome}"
            id_pai = st.selectbox("Conta Pai", options=list(opcoes_pai.keys()), format_func=lambda x: opcoes_pai[x])
            natureza = st.selectbox("Natureza", ["Ativo", "Passivo", "Patrimonio Liquido", "Receita", "Despesa"])
            if st.form_submit_button("Salvar"):
                if pc_controller.criar(id_pai, codigo, nome_plano, "", natureza):
                    st.success("Plano atualizado!")
                    st.rerun()

# ==========================================
# FUNÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    st.sidebar.title("EngFlow v1.0")
    st.sidebar.markdown("---")
    
    menu_options = {
        "Dashboards": ["Resumo Financeiro"],
        "Movimentacoes": ["Lancamentos"],
        "Cadastros": ["Pessoas", "Usuarios", "Contas Bancarias", "Plano de Contas", "Centro de Custo"],
        "Sistema": ["Configuracoes"]
    }
    
    flat_menu = []
    for category, options in menu_options.items():
        flat_menu.extend(options)
        
    choice = st.sidebar.selectbox("Selecione a Tela", flat_menu)
    st.sidebar.markdown("---")
    st.sidebar.info(f"Usuario: **Israel Silva**")

    if choice == "Lancamentos":
        exibir_tela_lancamentos()
    elif choice == "Resumo Financeiro":
        st.title("Painel de Controle")
        st.write("Em desenvolvimento: Graficos de Receita x Despesa.")
    elif choice == "Centro de Custo":
        exibir_tela_centro_custo()
    elif choice == "Pessoas":
        exibir_tela_pessoas()
    elif choice == "Usuarios":
        exibir_tela_usuarios()
    elif choice == "Contas Bancarias":
        exibir_tela_contas()
    elif choice == "Plano de Contas":
        exibir_tela_plano_contas()
    elif choice == "Configuracoes":
        st.title("Configuracoes")
        st.write("BD: SQL Server | Status: Conectado")

if __name__ == "__main__":
    main()
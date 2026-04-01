# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
from controllers.lancamento_controller import LancamentoController
from controllers.pessoa_controller import PessoaController
from controllers.conta_bancaria_controller import ContaBancariaController
from controllers.plano_contas_controller import PlanoContasController
from controllers.centro_custo_controller import CentroCustoController

def exibir_tela_lancamentos():
    st.title("Gestão de Lançamentos Financeiros")
    
    l_controller = LancamentoController()
    p_controller = PessoaController()
    cb_controller = ContaBancariaController()
    pc_controller = PlanoContasController()
    cc_controller = CentroCustoController()

    tab_lista, tab_novo = st.tabs(["Listar Lançamentos", "Novo Lançamento (Mestre/Detalhe)"])

    with tab_novo:
        st.subheader("1. Dados Principais (Mestre)")
        
        lista_pessoas = p_controller.listar_todos()
        lista_contas = cb_controller.listar_todos()
        lista_planos = pc_controller.listar_todos()
        lista_centros = cc_controller.listar_todos()

        with st.form("form_lancamento", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            pessoa_sel = col1.selectbox("Pessoa/Empresa", options=lista_pessoas, format_func=lambda x: x.nome_razao_social)
            conta_sel = col2.selectbox("Conta Bancária", options=lista_contas, format_func=lambda x: f"{x.codigo} - {x.numero}")
            tipo_doc = col3.selectbox("Tipo Documento", ["Boleto", "Nota Fiscal", "Recibo", "Transferência", "Pix"])

            col4, col5, col6 = st.columns(3)
            data_venc = col4.date_input("Data Vencimento", value=datetime.now())
            data_comp = col5.date_input("Data Competência", value=datetime.now())
            data_liq = col6.date_input("Data Liquidação (Opcional)", value=None)

            col7, col8, col9 = st.columns(3)
            vlr_bruto = col7.number_input("Valor Bruto", min_value=0.0, step=0.01, format="%.2f")
            vlr_liquido = col8.number_input("Valor Líquido", min_value=0.0, step=0.01, format="%.2f")
            status_sel = col9.selectbox("Status", ["Pendente", "Pago", "Agendado", "Cancelado"])

            st.markdown("---")
            st.subheader("2. Rateio (Detalhes)")
            
            # Chave "Observacao" sem acento para consistência interna
            df_rateio_input = pd.DataFrame([
                {"Plano de Contas": "", "Centro de Custo": "", "Valor Parcela": 0.0, "Observacao": ""}
            ])

            config_colunas = {
                "Plano de Contas": st.column_config.SelectboxColumn(options=[f"{p.codigo_contabil} - {p.nome}" for p in lista_planos], required=True),
                "Centro de Custo": st.column_config.SelectboxColumn(options=[c.centro_custo for c in lista_centros], required=True),
                "Valor Parcela": st.column_config.NumberColumn(format="R$ %.2f", min_value=0, required=True),
                "Observacao": st.column_config.TextColumn("Observação")
            }

            edicao_rateio = st.data_editor(
                df_rateio_input, 
                num_rows="dynamic", 
                column_config=config_colunas,
                use_container_width=True,
                key="editor_rateio"
            )

            btn_salvar = st.form_submit_button("Finalizar e Gravar Lançamento")

            if btn_salvar:
                df_final = pd.DataFrame(edicao_rateio)
                total_rateio = pd.to_numeric(df_final['Valor Parcela']).sum()

                if abs(total_rateio - vlr_bruto) > 0.01: # Tolerância para erros de float
                    st.error(f"Erro: A soma do rateio (R$ {total_rateio:.2f}) difere do valor bruto (R$ {vlr_bruto:.2f})")
                elif not pessoa_sel or vlr_bruto <= 0:
                    st.warning("Preencha os dados básicos corretamente.")
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
                        "criado_por": 1
                    }

                    lista_detalhes = []
                    try:
                        for _, row in df_final.iterrows():
                            if not row['Plano de Contas'] or not row['Centro de Custo']:
                                continue

                            p_cod = row['Plano de Contas'].split(" - ")[0]
                            id_pc = next(p.id for p in lista_planos if p.codigo_contabil == p_cod)
                            id_cc = next(c.id for c in lista_centros if c.centro_custo == row['Centro de Custo'])

                            lista_detalhes.append({
                                "id_plano_contas": id_pc,
                                "id_centro_custo": id_cc,
                                "valor_parcela": float(row['Valor Parcela']),
                                "observacao": row.get('Observacao', "")
                            })

                        if not lista_detalhes:
                            st.warning("Adicione as linhas de rateio.")
                        else:
                            with st.spinner("Gravando..."):
                                sucesso = l_controller.salvar_completo(dados_mestre, lista_detalhes)
                    
                            if sucesso:
                                # Mensagem de sucesso fora do form para garantir visibilidade
                                st.toast("Lançamento gravado com sucesso!", icon="✅")
                                st.success("Registro inserido. Limpando formulário...")
                                # O rerun forçado limpa o st.data_editor e os inputs do form
                                st.rerun()
                
                    except Exception as e:
                        st.error(f"Erro ao processar rateio: {e}")

    with tab_lista:
        st.subheader("Histórico de Lançamentos")
        historico = l_controller.listar_todos()
        if historico:
            df_hist = pd.DataFrame([
                {
                    "ID": h.id,
                    "Vencimento": h.data_vencimento,
                    "Valor Bruto": f"R$ {h.valor_bruto:,.2f}",
                    "Status": h.status,
                    "Documento": h.tipo_documento
                } for h in historico
            ])
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum lançamento encontrado.")
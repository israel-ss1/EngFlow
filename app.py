# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# Pega o caminho absoluto da pasta onde o app.py está
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

# Agora o Python VAI encontrar a pasta views
import streamlit as st

# 2. Agora importe as views usando o caminho absoluto do pacote
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from views.lancamentos_view import exibir_tela_lancamentos
    from views.pessoas_view import exibir_tela_pessoas
    from views.usuarios_view import exibir_tela_usuarios
    from views.contas_view import exibir_tela_contas
    from views.plano_contas_view import exibir_tela_plano_contas
    from views.centro_custo_view import exibir_tela_centro_custo
    from views.dashboard_view import exibir_tela_dashboard
except ModuleNotFoundError as e:
    st.error(f"Erro ao localizar módulos: {e}")
    st.stop()

# Configuração da página
st.set_page_config(page_title="EngFlow - Gestão Financeira", layout="wide")

def main():
    st.sidebar.title("EngFlow v1.0")
    st.sidebar.markdown("---")
    
    # 1. Usamos uma lista simples. A ordem aqui define a ordem no menu.
    # O primeiro item (índice 0) será o padrão ao abrir o app.
    menu_options = [
        "Resumo Financeiro", 
        "Lancamentos", 
        "Pessoas", 
        "Usuarios", 
        "Contas Bancarias", 
        "Plano de Contas", 
        "Centro de Custo", 
        "Configuracoes"
    ]
        
    # 2. Criamos o selectbox diretamente com a lista
    choice = st.sidebar.selectbox("Selecione a Tela", menu_options)
    st.sidebar.markdown("---")
    st.sidebar.info(f"Usuario: **Israel Silva**")

    # 3. Roteamento (Lógica de decisão)
    if choice == "Resumo Financeiro":
        exibir_tela_dashboard()
    elif choice == "Lancamentos":
        exibir_tela_lancamentos()
    elif choice == "Pessoas":
        exibir_tela_pessoas()
    elif choice == "Centro de Custo":
        exibir_tela_centro_custo()
    elif choice == "Usuarios":
        exibir_tela_usuarios()
    elif choice == "Contas Bancarias":
        exibir_tela_contas()
    elif choice == "Plano de Contas":
        exibir_tela_plano_contas()
    elif choice == "Configuracoes":
        st.title("Configurações")
        st.write("BD: SQL Server | Status: Conectado")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
from controllers.usuario_controller import UsuarioController

def exibir_tela_usuarios():
    st.title("Gestão de Usuários")
    u_controller = UsuarioController()
    tab_lista, tab_novo = st.tabs(["Listar Usuários", "Novo Usuário"])
    with tab_novo:
        with st.form("form_usuario", clear_on_submit=True):
            nome_u = st.text_input("Nome Completo")
            email_u = st.text_input("E-mail")
            senha_u = st.text_input("Senha", type="password")
            papel_u = st.selectbox("Perfil", ["Administrador", "Gerente", "Operador", "Leitura"])
            if st.form_submit_button("Cadastrar"):
                if u_controller.criar(nome_u, email_u, senha_u, papel_u):
                    st.success("Usuário criado!")
                    st.rerun()
    with tab_lista:
        usuarios = u_controller.listar_todos() # Supondo que exista este método
        if usuarios:
             df = pd.DataFrame([{"Nome": u.nome, "Email": u.email, "Perfil": u.papel} for u in usuarios])
             st.dataframe(df, use_container_width=True)
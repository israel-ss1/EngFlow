# -*- coding: utf-8 -*-
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnection:
    """
    Gerencia a conexão com o PostgreSQL utilizando o cache do Streamlit.
    Ideal para o projeto EngFlow no Streamlit Cloud.
    """
    
    @st.cache_resource
    def get_engine(_self):
        try:
            # Busca as credenciais em st.secrets["connections"]["postgresql"]
            creds = st.secrets["connections"]["postgresql"]
            
            # Formata a URL para o driver psycopg2
            connection_url = (
                f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{creds['database']}?sslmode=require"
            )

            engine = create_engine(
                connection_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
            
            # Teste rápido de conexão
            with engine.connect() as conn:
                pass
                
            return engine
        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def get_session(self):
        engine = self.get_engine()
        if engine:
            Session = sessionmaker(bind=engine)
            return Session()
        return None

# Instância global para facilitar o acesso
db_manager = DatabaseConnection()
engine = db_manager.get_engine()
# -*- coding: utf-8 -*-
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from threading import Lock

class DatabaseConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.engine = None
        self.Session = None
        
        try:
            # Pegando as credenciais dos Secrets do Streamlit
            creds = st.secrets["connections"]["postgresql"]
            
            user = creds["username"]     
            pwd = creds["password"]      
            host = creds["host"]        
            port = 6543 # Porta do Pooler (Transaction)
            db = creds["database"]      

            # URL com o driver psycopg2 e porta correta
            connection_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"

            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                # Resolve o erro de "Cannot assign requested address" no Cloud
                connect_args={"gssencmode": "disable"} 
            )
            
            self.Session = sessionmaker(bind=self.engine)
            
            # Teste rápido para validar a conexão
            with self.engine.connect() as conn:
                self._initialized = True
                
        except Exception as e:
            # Log do erro para depuração
            st.error(f"Erro de conexão no banco: {e}")

    def get_session(self):
        if self.Session is None:
            return None
        return self.Session()

# --- EXPORTAÇÃO GLOBAL ---
# Isso resolve o erro de "name 'engine' is not defined" nos outros arquivos
db_inst = DatabaseConnection()
engine = db_inst.engine
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from threading import Lock
import streamlit as st

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
            # Buscando as credenciais do st.secrets
            creds = st.secrets["connections"]["postgresql"]
            
            user = creds["username"]     
            pwd = creds["password"]      
            host = creds["host"]        
            port = 6543 # Porta do Pooler do Supabase
            db = creds["database"]      

            # URL com driver explícito e porta correta
            connection_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"

            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                # Resolve o erro de endereço no Streamlit Cloud
                connect_args={"gssencmode": "disable"} 
            )
            
            self.Session = sessionmaker(bind=self.engine)
            
            # Teste de conexão rápido
            with self.engine.connect() as conn:
                self._initialized = True
                
        except Exception as e:
            # Não marcamos como inicializado para tentar novamente no próximo rerun
            st.error(f"Erro crítico de conexão: {e}")

    def get_session(self):
        if self.Session is None:
            return None
        return self.Session()

# --- EXPOSIÇÃO DA VARIÁVEL ---
# Cria a instância única (Singleton)
db_connection = DatabaseConnection()

# Expõe o engine para que os controllers possam importar
engine = db_connection.engine
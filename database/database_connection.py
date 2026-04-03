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
            # Pega os dados dos Secrets (aqueles que você achou no Supabase)
            creds = st.secrets["connections"]["postgresql"]
            
            user = creds["username"]     
            pwd = creds["password"]      
            host = creds["host"]        
            port = 6543 # Porta do Pooler/Transaction
            db = creds["database"]      

            # A URL com o driver psycopg2 e a porta 6543
            connection_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"

            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                # Resolve o erro "Cannot assign requested address" no Cloud
                connect_args={"gssencmode": "disable"} 
            )
            
            self.Session = sessionmaker(bind=self.engine)
            
            with self.engine.connect() as conn:
                self._initialized = True
                
        except Exception as e:
            st.error(f"Erro crítico de conexão: {e}")

    def get_session(self):
        if self.Session is None:
            return None
        return self.Session()

# --- ESTA PARTE É FUNDAMENTAL E FICA FORA DA CLASSE ---
# Ela cria a variável global que os outros arquivos vão importar
db_connection = DatabaseConnection()
engine = db_connection.engine
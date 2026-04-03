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
            # Puxa os dados atualizados do st.secrets
            creds = st.secrets["connections"]["postgresql"]
            
            user = creds["username"]     
            pwd = creds["password"]      
            host = creds["host"]         # Deve ser o endereço do 'pooler'
            port = int(creds["port"])    # Garante que é um inteiro (6543)
            db = creds["database"]      

            # URL utilizando o driver psycopg2 e a porta de transação
            connection_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"

            # Criação do engine com ajustes para o Streamlit Cloud
            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                # Resolve o erro "Cannot assign requested address" e problemas de rede
                connect_args={
                    "gssencmode": "disable",
                    "connect_timeout": 10
                }
            )
            
            self.Session = sessionmaker(bind=self.engine)
            
            # Validação rápida da conexão
            with self.engine.connect() as conn:
                self._initialized = True
                
        except Exception as e:
            # Exibe o erro na interface para facilitar o seu debug
            st.error(f"Erro ao conectar no banco de dados: {e}")

    def get_session(self):
        if self.Session is None:
            return None
        return self.Session()

# --- EXPORTAÇÃO PARA O PROJETO ---
# Instancia o Singleton assim que o módulo é importado
db_inst = DatabaseConnection()

# Expõe o engine para ser usado em pd.read_sql ou nos controllers
# Isso resolve o erro "name 'engine' is not defined"
engine = db_inst.engine
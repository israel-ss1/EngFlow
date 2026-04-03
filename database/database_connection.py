# -*- coding: latin-1 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from threading import Lock
import streamlit as st # Importante para ler as credenciais

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
            
        # Garantir que os atributos existam mesmo se a conexao falhar
        self.engine = None
        self.Session = None
        
        try:
            # Buscando as credenciais do .streamlit/secrets.toml
            # Certifique-se de que o nome no TOML seja [connections.postgresql]
            creds = st.secrets["connections"]["postgresql"]
            
            user = creds["username"]     # No Supabase geralmente é 'postgres'
            pwd = creds["password"]      # Sua senha do banco
            host = creds["host"]        # Algo como db.xxxx.supabase.co
            port = creds["port"]        # Geralmente 5432
            db = creds["database"]      # No Supabase é sempre 'postgres'

            # Nova URL para PostgreSQL
            # Usamos o driver padrão do Postgres (psycopg2)
            #connection_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"
            # Adicione "+psycopg2" logo após "postgresql"
            connection_url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"
            
            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                echo=False,
                pool_size=5,
                max_overflow=10,
                # ESTA LINHA ABAIXO É A CHAVE PARA O ERRO "Cannot assign requested address"
                connect_args={"gssencmode": "disable"} 
            )
            
            # Tenta criar a fabrica de sessoes
            self.Session = sessionmaker(bind=self.engine)
            
            # TESTE REAL: Verifica se a conexão está ativa
            with self.engine.connect() as conn:
                self._initialized = True
                print("--- Conexao Supabase/PostgreSQL OK! ---")
                
        except Exception as e:
            self._initialized = True
            self.Session = None 
            # Isso vai forçar o erro a aparecer na interface do Streamlit
            st.error(f"Erro crítico de conexão: {e}")


    def get_session(self):
        if self.Session is None:
            return None
        return self.Session()
    
# No final do arquivo database_connection.py
db_instance = DatabaseConnection()
engine = db_instance.engine  # Isso expõe a variável para outros arquivos
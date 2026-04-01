# -*- coding: latin-1 -*-
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
            
        # Garantir que os atributos existam mesmo se a conexao falhar
        self.engine = None
        self.Session = None
        
        user = 'sa'
        pwd = 'admin123'
        server = 'DESKTOP-LO3B79V'
        db = 'EngFlow'
        # Adicionado TrustServerCertificate=yes para evitar erros de SSL locais
        driver = 'ODBC+Driver+17+for+SQL+Server'

        # URL com parametros de seguranca para conexao local
        connection_url = f"mssql+pyodbc://{user}:{pwd}@{server}/{db}?driver={driver}&TrustServerCertificate=yes"

        try:
            self.engine = create_engine(
                connection_url, 
                pool_pre_ping=True,
                echo=False
            )
            # Tenta criar a fabrica de sessoes
            self.Session = sessionmaker(bind=self.engine)
            
            # TESTE REAL: Se falhar aqui, o 'except' captura
            with self.engine.connect() as conn:
                self._initialized = True
                print("--- Conexao SQLAlchemy OK! ---")
        except Exception as e:
            self._initialized = False
            self.Session = None # Garante que continue None para sabermos que falhou
            print(f"ERRO DE CONEXAO: {e}")

    def get_session(self):
        if self.Session is None:
            # Em vez de quebrar, retornamos None ou levantamos um erro amigavel
            return None
        return self.Session()
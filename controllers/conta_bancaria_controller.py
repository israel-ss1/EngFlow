# -*- coding: latin-1 -*-
from database.database_connection import DatabaseConnection
from entities.conta_bancaria import ContaBancaria

class ContaBancariaController:
    def __init__(self):
        self.db = DatabaseConnection()

    def criar(self, codigo, numero, tipo):
        session = self.db.get_session()
        if session is None:
            return False
            
        try:
            nova_conta = ContaBancaria(codigo=codigo, numero=numero, tipo=tipo)
            session.add(nova_conta)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir conta: {e}")
            return False
        finally:
            if session:
                session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None:
            return []
            
        try:
            return session.query(ContaBancaria).order_by(ContaBancaria.codigo).all()
        finally:
            if session:
                session.close()

    def deletar(self, id_item):
        session = self.db.get_session()
        if session is None:
            return False
            
        try:
            item = session.query(ContaBancaria).filter(ContaBancaria.id == id_item).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            return False
        finally:
            if session:
                session.close()
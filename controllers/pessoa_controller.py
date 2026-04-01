# -*- coding: utf-8 -*-
from database.database_connection import DatabaseConnection
from entities.pessoa import Pessoa

class PessoaController:
    def __init__(self):
        self.db = DatabaseConnection()

    def criar(self, nome, cpf_cnpj):
        session = self.db.get_session()
        if session is None: return False
        try:
            novo_registro = Pessoa(
                nome_razao_social=nome,
                cpf_cnpj=cpf_cnpj
            )
            session.add(novo_registro)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir em pessoa: {e}")
            return False
        finally:
            if session:
                session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None: return []
        try:
            return session.query(Pessoa).order_by(Pessoa.nome_razao_social).all()
        finally:
            if session:
                session.close()

    def deletar(self, id_item):
        session = self.db.get_session()
        if session is None: return False
        try:
            item = session.query(Pessoa).filter(Pessoa.id == id_item).first()
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
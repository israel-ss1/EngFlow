# -*- coding: latin-1 -*-
from database.database_connection import DatabaseConnection
from entities.plano_contas import PlanoContas

class PlanoContasController:
    def __init__(self):
        self.db = DatabaseConnection()

    def criar(self, id_pai, codigo, nome, descricao, natureza):
        session = self.db.get_session()
        if session is None: return False
        try:
            nova_conta = PlanoContas(
                id_pai=id_pai if id_pai != 0 else None,
                codigo_contabil=codigo,
                nome=nome,
                descricao=descricao,
                natureza=natureza
            )
            session.add(nova_conta)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir no Plano de Contas: {e}")
            return False
        finally:
            if session:
                session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None: return []
        try:
            return session.query(PlanoContas).order_by(PlanoContas.codigo_contabil).all()
        finally:
            if session:
                session.close()
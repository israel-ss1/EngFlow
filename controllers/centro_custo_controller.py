# -*- coding: latin-1 -*-
# ALTERADO: Agora apontamos para a pasta correta
from database.database_connection import DatabaseConnection
from entities.centro_custo import CentroCusto

class CentroCustoController:
    def __init__(self):
        self.db = DatabaseConnection()

    def criar(self, nome, descricao, codigo):
        session = self.db.get_session()
        if session is None:
            return False
            
        try:
            novo_item = CentroCusto(centro_custo=nome, descricao=descricao, codigo=codigo)
            session.add(novo_item)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir: {e}")
            return False
        finally:
            # So tenta fechar se a sessao foi criada com sucesso
            if session:
                session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None:
            return []
            
        try:
            return session.query(CentroCusto).order_by(CentroCusto.centro_custo).all()
        finally:
            if session:
                session.close()

    def deletar(self, id_item):
        session = self.db.get_session()
        try:
            item = session.query(CentroCusto).filter(CentroCusto.id == id_item).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()
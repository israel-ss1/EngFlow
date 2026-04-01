# -*- coding: utf-8 -*-
from database.database_connection import DatabaseConnection
from entities.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.db = DatabaseConnection()

    def criar(self, nome, email, hash_senha, papel):
        session = self.db.get_session()
        if session is None: return False
        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                hash_senha=hash_senha,
                papel=papel
            )
            session.add(novo_usuario)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir usuario: {e}")
            return False
        finally:
            if session:
                session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None: return []
        try:
            return session.query(Usuario).order_by(Usuario.nome).all()
        finally:
            if session:
                session.close()

    def deletar(self, id_item):
        session = self.db.get_session()
        if session is None: return False
        try:
            user = session.query(Usuario).filter(Usuario.id == id_item).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            return False
        finally:
            if session:
                session.close()
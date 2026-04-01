# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from entities.base import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    hash_senha = Column(String(100), nullable=False)
    papel = Column(String(50)) # Ex: Admin, Operador, Consulta
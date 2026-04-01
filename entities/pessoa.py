# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from entities.base import Base

class Pessoa(Base):
    __tablename__ = 'pessoa'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_razao_social = Column(String(150), nullable=False)
    cpf_cnpj = Column(String(50))
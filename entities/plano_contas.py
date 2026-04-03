# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from entities.base import Base

class PlanoContas(Base):
    __tablename__ = 'plano_contas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pai = Column(Integer, ForeignKey('plano_contas.id'), nullable=True)
    codigo_contabil = Column(String(15), nullable=False)
    nome = Column(String(20), nullable=False)
    descricao = Column(String(250))
    natureza = Column(String(15), nullable=False)

    # Relacionamento para facilitar navegação na árvore
    pai = relationship("PlanoContas", remote_side=[id], backref="filhos")
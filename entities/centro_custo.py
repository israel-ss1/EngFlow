# -*- coding: latin-1 -*-
from sqlalchemy import Column, Integer, String
from entities.base import Base

class CentroCusto(Base):
    __tablename__ = 'centro_custo'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    centro_custo = Column(String(50), nullable=False)
    descricao = Column(String(50))
    codigo = Column(String(15), nullable=False)
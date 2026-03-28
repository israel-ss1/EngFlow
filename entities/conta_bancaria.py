# -*- coding: latin-1 -*-
from sqlalchemy import Column, Integer, String
from entities.base import Base

class ContaBancaria(Base):
    __tablename__ = 'conta_bancaria'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(5), nullable=False)
    numero = Column(String(15), nullable=False)
    tipo = Column(String(20))
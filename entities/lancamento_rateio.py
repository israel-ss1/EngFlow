# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from entities.base import Base

class LancamentoRateio(Base):
    __tablename__ = 'lancamento_rateio'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_lancamento = Column(Integer, ForeignKey('lancamento.id', ondelete="CASCADE"), nullable=False)
    id_plano_contas = Column(Integer, ForeignKey('plano_contas.id'), nullable=False)
    id_centro_custo = Column(Integer, ForeignKey('centro_custo.id'), nullable=False)
    valor_parcela = Column(Numeric(19, 4), nullable=False)
    observacao = Column(String(250))
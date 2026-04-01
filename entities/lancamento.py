# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from entities.base import Base
from datetime import datetime

class Lancamento(Base):
    __tablename__ = 'lancamento'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pessoa = Column(Integer, ForeignKey('pessoa.id'), nullable=False)
    id_conta_bancaria = Column(Integer, ForeignKey('conta_bancaria.id'), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_competencia = Column(Date, nullable=False)
    data_liquidacao = Column(Date, nullable=True)
    valor_bruto = Column(Numeric(19, 4), nullable=False)
    valor_liquido = Column(Numeric(19, 4), nullable=False)
    status = Column(String(30), nullable=False, default='Pendente')
    tipo_documento = Column(String(30), nullable=False)
    criado_por = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    criado_em = Column(Date, nullable=False, default=datetime.now)
    atualizado_por = Column(Integer, ForeignKey('usuario.id'))
    atualizado_em = Column(Date)

    # Relacionamento para acessar os itens de rateio
    rateios = relationship("LancamentoRateio", backref="lancamento", cascade="all, delete-orphan")
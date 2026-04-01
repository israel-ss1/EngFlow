# -*- coding: utf-8 -*-
from database.database_connection import DatabaseConnection
from entities.lancamento import Lancamento
from entities.lancamento_rateio import LancamentoRateio

class LancamentoController:
    def __init__(self):
        self.db = DatabaseConnection()

    def salvar_completo(self, dados_mestre, lista_rateio):
        session = self.db.get_session()
        if session is None: return False
        try:
            # 1. Cria o objeto mestre
            novo_lancamento = Lancamento(**dados_mestre)
            session.add(novo_lancamento)
            session.flush() # Gera o ID do lancamento sem commitar ainda

            # 2. Cria os rateios vinculados ao ID gerado
            for item in lista_rateio:
                novo_rateio = LancamentoRateio(
                    id_lancamento=novo_lancamento.id,
                    id_plano_contas=item['id_plano_contas'],
                    id_centro_custo=item['id_centro_custo'],
                    valor_parcela=item['valor_parcela'],
                    observacao=item.get('observacao')
                )
                session.add(novo_rateio)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro na transacao de lancamento: {e}")
            return False
        finally:
            session.close()

    def listar_todos(self):
        session = self.db.get_session()
        if session is None: return []
        try:
            return session.query(Lancamento).order_by(Lancamento.data_vencimento.desc()).all()
        finally:
            session.close()
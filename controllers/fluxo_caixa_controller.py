# -*- coding: latin-1 -*-
from database.database_connection import DatabaseConnection
from datetime import datetime
from sqlalchemy import text

class FluxoCaixaController:
    def __init__(self):
        self.db = DatabaseConnection()

    def registrar_lancamento(self, descricao: str, valor: float, tipo: str, categoria: str):
        sql = text("""
            INSERT INTO Lancamentos (Descricao, Valor, Tipo, Categoria, DataLancamento)
            VALUES (:desc, :val, :tipo, :cat, :data)
        """)
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with self.db.engine.connect() as conn:
            conn.execute(sql, {
                "desc": descricao, 
                "val": valor, 
                "tipo": tipo, 
                "cat": categoria, 
                "data": data_atual
            })
            conn.commit()

    def listar_todos(self):
        sql = text("SELECT Id, Descricao, Valor, Tipo, Categoria, DataLancamento FROM Lancamentos ORDER BY DataLancamento DESC")
        with self.db.engine.connect() as conn:
            result = conn.execute(sql)
            return result.fetchall()

    def obtener_resumo_financeiro(self):
        sql = text("""
            SELECT 
                SUM(CASE WHEN Tipo = 'Receita' THEN Valor ELSE 0 END) as receitas,
                SUM(CASE WHEN Tipo = 'Despesa' THEN Valor ELSE 0 END) as despesas
            FROM Lancamentos
        """)
        with self.db.engine.connect() as conn:
            resultado = conn.execute(sql).fetchone()
            
        if resultado:
            receitas = float(resultado[0] or 0.0)
            despesas = float(resultado[1] or 0.0)
            return {
                "receitas": receitas,
                "despesas": despesas,
                "saldo": receitas - despesas
            }
        return {"receitas": 0, "despesas": 0, "saldo": 0}

    def deletar_lancamento(self, id_lancamento: int):
        sql = text("DELETE FROM Lancamentos WHERE Id = :id")
        with self.db.engine.connect() as conn:
            conn.execute(sql, {"id": id_lancamento})
            conn.commit()
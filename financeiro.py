import json
import os
from datetime import datetime


ARQUIVO_DADOS = "dados.json"


class GerenciadorFinanceiro:
    def __init__(self):
        self.transacoes = []
        self.proximo_id = 1
        self.carregar()

    def carregar(self):
        """Carrega transações do arquivo JSON"""
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    self.transacoes = dados.get("transacoes", [])
                    self.proximo_id = dados.get("proximo_id", 1)
            except (json.JSONDecodeError, KeyError):
                print("Aviso: erro ao ler dados, iniciando com lista vazia.")
                self.transacoes = []
                self.proximo_id = 1

    def salvar(self):
        """Salva transações no arquivo JSON"""
        dados = {
            "transacoes": self.transacoes,
            "proximo_id": self.proximo_id
        }
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def adicionar(self, tipo, descricao, valor, categoria, data):
        transacao = {
            "id": self.proximo_id,
            "tipo": tipo,
            "descricao": descricao,
            "valor": round(valor, 2),
            "categoria": categoria,
            "data": data,
            "criado_em": datetime.now().isoformat()
        }
        self.transacoes.append(transacao)
        self.proximo_id += 1
        self.salvar()
        return transacao

    def remover(self, id_transacao):
        for i, t in enumerate(self.transacoes):
            if t["id"] == id_transacao:
                self.transacoes.pop(i)
                self.salvar()
                return True
        return False

    def listar_todas(self):
        return sorted(self.transacoes, key=lambda x: self._parse_data(x["data"]), reverse=True)

    def buscar(self, termo):
        termo_lower = termo.lower()
        resultados = []
        for t in self.transacoes:
            if (termo_lower in t["descricao"].lower() or
                    termo_lower in t["categoria"].lower()):
                resultados.append(t)
        return resultados

    def resumo_mes(self, mes, ano):
        transacoes_mes = []
        for t in self.transacoes:
            data = self._parse_data(t["data"])
            if data and data.month == mes and data.year == ano:
                transacoes_mes.append(t)

        receitas = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "receita")
        despesas = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "despesa")

        maior_despesa = 0
        for t in transacoes_mes:
            if t["tipo"] == "despesa" and t["valor"] > maior_despesa:
                maior_despesa = t["valor"]

        return {
            "receitas": receitas,
            "despesas": despesas,
            "saldo": receitas - despesas,
            "total_transacoes": len(transacoes_mes),
            "maior_despesa": maior_despesa
        }

    def relatorio_por_categoria(self):
        if not self.transacoes:
            return {}

        relatorio = {}
        for t in self.transacoes:
            tipo = t["tipo"]
            cat = t["categoria"]

            if tipo not in relatorio:
                relatorio[tipo] = {}
            if cat not in relatorio[tipo]:
                relatorio[tipo][cat] = 0

            relatorio[tipo][cat] += t["valor"]

        return relatorio

    def _parse_data(self, data_str):
        """Converte string de data para objeto datetime"""
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except (ValueError, TypeError):
            return None

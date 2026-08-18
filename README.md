# 💰 Gerenciador Financeiro Pessoal

Sistema de gerenciamento financeiro via terminal feito em Python. Permite controlar receitas e despesas, visualizar resumos mensais e gerar relatórios por categoria.

Projeto desenvolvido durante o 2º semestre de Ciência da Computação na FIAP.

## Funcionalidades

- Cadastro de receitas e despesas com categorias
- Listagem de todas as transações
- Resumo financeiro mensal (receitas, despesas, saldo)
- Relatório por categoria com porcentagem e gráfico no terminal
- Busca de transações por descrição ou categoria
- Remoção de transações
- Dados salvos automaticamente em JSON

## Como rodar

```bash
# clone o repositório
git clone https://github.com/Eduardomors/gerenciador-financeiro.git
cd gerenciador-financeiro

# execute
python main.py
```

Precisa ter Python 3.8+ instalado. Não usa nenhuma biblioteca externa.

## Estrutura

```
├── main.py          # Interface do menu e interação com usuário
├── financeiro.py    # Classe principal com lógica de negócio
├── dados.json       # Arquivo de dados (criado automaticamente)
└── README.md
```

## Preview

```
=============================================
   GERENCIADOR FINANCEIRO PESSOAL
=============================================
[1] Adicionar receita
[2] Adicionar despesa
[3] Listar transações
[4] Resumo do mês
[5] Relatório por categoria
[6] Remover transação
[7] Buscar transações
[0] Sair
---------------------------------------------
```

## Aprendizados

- Manipulação de arquivos JSON pra persistência de dados
- Orientação a objetos (encapsulamento, organização em módulos)
- Tratamento de exceções e validação de entrada
- Formatação de strings e saída formatada no terminal

## Melhorias futuras

- [ ] Exportar relatórios em CSV
- [ ] Adicionar gráficos com matplotlib
- [ ] Filtro por período customizado
- [ ] Metas de gastos por categoria

---

Feito por [Eduardo Moreira](https://github.com/Eduardomors)

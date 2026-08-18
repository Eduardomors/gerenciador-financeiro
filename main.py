from financeiro import GerenciadorFinanceiro
from datetime import datetime
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_menu():
    print("\n" + "=" * 45)
    print("   GERENCIADOR FINANCEIRO PESSOAL")
    print("=" * 45)
    print("[1] Adicionar receita")
    print("[2] Adicionar despesa")
    print("[3] Listar transações")
    print("[4] Resumo do mês")
    print("[5] Relatório por categoria")
    print("[6] Remover transação")
    print("[7] Buscar transações")
    print("[0] Sair")
    print("-" * 45)


def ler_valor():
    while True:
        try:
            valor = float(input("Valor (R$): ").replace(",", "."))
            if valor <= 0:
                print("O valor precisa ser positivo.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Use números (ex: 150.50)")


def ler_data():
    data_input = input("Data (dd/mm/aaaa) ou Enter para hoje: ").strip()
    if not data_input:
        return datetime.now().strftime("%d/%m/%Y")
    try:
        datetime.strptime(data_input, "%d/%m/%Y")
        return data_input
    except ValueError:
        print("Data inválida, usando data de hoje.")
        return datetime.now().strftime("%d/%m/%Y")


CATEGORIAS_RECEITA = ["Salário", "Freelance", "Investimentos", "Outros"]
CATEGORIAS_DESPESA = [
    "Alimentação", "Transporte", "Moradia", "Educação",
    "Lazer", "Saúde", "Compras", "Outros"
]


def escolher_categoria(tipo):
    categorias = CATEGORIAS_RECEITA if tipo == "receita" else CATEGORIAS_DESPESA
    print("\nCategorias:")
    for i, cat in enumerate(categorias, 1):
        print(f"  [{i}] {cat}")

    while True:
        try:
            opcao = int(input("Escolha a categoria: "))
            if 1 <= opcao <= len(categorias):
                return categorias[opcao - 1]
            print("Opção inválida.")
        except ValueError:
            print("Digite um número.")


def adicionar_transacao(gerenciador, tipo):
    print(f"\n--- Nova {tipo.upper()} ---")
    descricao = input("Descrição: ").strip()
    if not descricao:
        print("Descrição não pode ser vazia.")
        return

    valor = ler_valor()
    categoria = escolher_categoria(tipo)
    data = ler_data()

    gerenciador.adicionar(tipo, descricao, valor, categoria, data)
    print(f"\n✓ {tipo.capitalize()} de R${valor:.2f} adicionada com sucesso!")


def listar_transacoes(gerenciador):
    transacoes = gerenciador.listar_todas()
    if not transacoes:
        print("\nNenhuma transação registrada ainda.")
        return

    print(f"\n{'ID':<5} {'Tipo':<10} {'Descrição':<20} {'Valor':>10} {'Categoria':<15} {'Data':<12}")
    print("-" * 75)

    for t in transacoes:
        sinal = "+" if t["tipo"] == "receita" else "-"
        print(f"{t['id']:<5} {t['tipo']:<10} {t['descricao']:<20} {sinal}R${t['valor']:>8.2f} {t['categoria']:<15} {t['data']:<12}")


def resumo_mensal(gerenciador):
    mes_input = input("\nMês/Ano (mm/aaaa) ou Enter para mês atual: ").strip()
    if not mes_input:
        agora = datetime.now()
        mes, ano = agora.month, agora.year
    else:
        try:
            partes = mes_input.split("/")
            mes, ano = int(partes[0]), int(partes[1])
        except (ValueError, IndexError):
            print("Formato inválido.")
            return

    resumo = gerenciador.resumo_mes(mes, ano)

    print(f"\n{'=' * 40}")
    print(f"  RESUMO - {mes:02d}/{ano}")
    print(f"{'=' * 40}")
    print(f"  Receitas:  R$ {resumo['receitas']:>10.2f}")
    print(f"  Despesas:  R$ {resumo['despesas']:>10.2f}")
    print(f"  {'─' * 30}")

    saldo = resumo['saldo']
    status = "✓" if saldo >= 0 else "✗"
    print(f"  Saldo:     R$ {saldo:>10.2f}  {status}")
    print(f"{'=' * 40}")

    if resumo['total_transacoes'] > 0:
        print(f"\n  Total de transações: {resumo['total_transacoes']}")
        print(f"  Maior despesa: R$ {resumo['maior_despesa']:.2f}")


def relatorio_categorias(gerenciador):
    relatorio = gerenciador.relatorio_por_categoria()
    if not relatorio:
        print("\nNenhuma transação registrada.")
        return

    print(f"\n{'=' * 50}")
    print("  RELATÓRIO POR CATEGORIA")
    print(f"{'=' * 50}")

    for tipo in ["receita", "despesa"]:
        if tipo in relatorio:
            print(f"\n  {tipo.upper()}S:")
            total_tipo = sum(relatorio[tipo].values())
            for cat, valor in sorted(relatorio[tipo].items(), key=lambda x: x[1], reverse=True):
                porcentagem = (valor / total_tipo) * 100
                barra = "█" * int(porcentagem / 5)
                print(f"    {cat:<15} R${valor:>9.2f}  {porcentagem:>5.1f}%  {barra}")


def remover_transacao(gerenciador):
    listar_transacoes(gerenciador)
    try:
        id_remover = int(input("\nID da transação para remover: "))
        confirmacao = input("Tem certeza? (s/n): ").strip().lower()
        if confirmacao == 's':
            if gerenciador.remover(id_remover):
                print("✓ Transação removida.")
            else:
                print("ID não encontrado.")
    except ValueError:
        print("ID inválido.")


def buscar_transacoes(gerenciador):
    termo = input("\nBuscar por (descrição ou categoria): ").strip()
    if not termo:
        return

    resultados = gerenciador.buscar(termo)
    if not resultados:
        print("Nenhuma transação encontrada.")
        return

    print(f"\nEncontradas {len(resultados)} transação(ões):")
    for t in resultados:
        sinal = "+" if t["tipo"] == "receita" else "-"
        print(f"  {t['data']} | {t['descricao']:<20} | {sinal}R${t['valor']:.2f} | {t['categoria']}")


def main():
    gerenciador = GerenciadorFinanceiro()
    print("\nBem-vindo ao Gerenciador Financeiro!")

    while True:
        exibir_menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            adicionar_transacao(gerenciador, "receita")
        elif opcao == "2":
            adicionar_transacao(gerenciador, "despesa")
        elif opcao == "3":
            listar_transacoes(gerenciador)
        elif opcao == "4":
            resumo_mensal(gerenciador)
        elif opcao == "5":
            relatorio_categorias(gerenciador)
        elif opcao == "6":
            remover_transacao(gerenciador)
        elif opcao == "7":
            buscar_transacoes(gerenciador)
        elif opcao == "0":
            gerenciador.salvar()
            print("\nDados salvos. Até mais! 👋")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

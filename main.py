import sys
import os

from tabuleiro import (
    limpar_tela, imprimeNonograma, MAGENTA, YELLOW, BOLD, RED, BG_GREEN
)
from metodos import resolver_backtracking, resolver_genetico, resolver_hibrido


def exibir_resultado(
    jogo: list,
    linha: int,
    coluna: int,
    nL: list,
    nC: list,
    maiorL: int,
    maiorC: int,
    cabecalhoL_visual: list,
    cabecalhoC: list,
    resultado_solver: any,
    algoritmo: str
) -> None:
    # 1. Limpa a tela e exibe a identidade visual
    limpar_tela()
    menu()
    
    # 2. Imprime o tabuleiro completamente resolvido
    imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC)
    print(BOLD("\nPROCESSO FINALIZADO!"))
    
    # 3. Cabeçalho do Relatório de Métricas
    print(f"\n{BOLD('MÉTRICAS — ' + algoritmo.upper())}")
    print("─" * 52)

    # Se o solver retornar o dicionário correto com as métricas
    if isinstance(resultado_solver, dict) and "metrics" in resultado_solver:
        metrics_data = resultado_solver["metrics"]
        
        # Imprime cada chave e valor perfeitamente alinhados à esquerda e direita
        for chave, valor in metrics_data.items():
            print(f"  {chave:<26} {valor:>20}")
            
    else:
        # Fallback caso o solver ainda esteja retornando apenas True/False (o seu caso atual)
        status_txt = "Sim" if resultado_solver is True else "Não"
        print(f"  {'Algoritmo':<26} {algoritmo:>20}")
        print(f"  {'Dimensões':<26} {f'{linha}x{coluna}':>20}")
        print(f"  {'Resolvido':<26} {status_txt:>20}")
        print("─" * 52)
        print(RED("  ⚠ Atenção: Modifique o retorno do seu solver em 'metodos.py'"))
        print(RED("  para devolver o dicionário gerado pelo Metrics.build()."))
        
    print("─" * 52)
    print()


def menu():
    # Exibe a Logo ASCII 
    print(MAGENTA("""
    ███╗   ██╗ ██████╗ ███╗   ██╗ ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗ █████╗
    ████╗  ██║██╔═══██╗████╗  ██║██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║██╔══██╗
    ██╔██╗ ██║██║   ██║██╔██╗ ██║██║   ██║██║   ███╗██████╔╝███████║██╔████╔██║███████║
    ██║╚██╗██║██║   ██║██║╚██╗██║██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══██║
    ██║ ╚████║╚██████╔╝██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║
    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝
    """))


def comandos(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC):
    while True:
        print(BG_GREEN("                      MÉTODOS DE RESOLUÇÃO                      ".center(75)))
        print()
        print(f"{'Opção':<12}                                       Descrição")
        print("-"*75)
        print(f"{MAGENTA('1'):<12}{'Backtracking ':<32}  Busca exata recursiva com podas heurísticas")
        print(f"{YELLOW('2'):<12}{'Algoritmo Genético':<32}  Evolução populacional por busca estocástica")
        print(f"{BOLD('3'):<12}{'Método Híbrido':<32} Processamento AG → Refinamento por Backtracking")
        print(f"{BOLD('sair'):<12}                                 {'Encerra o Programa':<32}")
        print()

        entrada = input(BOLD("Escolha uma opção (1, 2, 3) ou digite 'sair': ")).strip().lower()
        
        if not entrada:
            continue

        if entrada == "sair":
            limpar_tela()
            print(BOLD("Obrigado por jogar ") + MAGENTA("<3") + BOLD("!"))
            break
            
        elif entrada in ["1", "2", "3"]:
            if entrada == "1":
                res = resolver_backtracking(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "BT")
            elif entrada == "2":
                res = resolver_genetico(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "AG")
            elif entrada == "3":
                res = resolver_hibrido(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "HD")
            break
        else:
            limpar_tela()
            menu()
            imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC)
            print(RED("\nOpção Inválida! Escolha 1, 2, 3 ou digite 'sair'.\n"))


def main():
    if len(sys.argv) == 1:
        arq = input("Por favor, digite o nome do arquivo do nonograma (ex: instancias/nonogram_5x5.txt):\n").strip()
        limpar_tela()
    else:
        arq = sys.argv[1]

    try:
        with open(arq, "r", encoding="utf-8") as file:
            linhas_arquivo = [l.strip() for l in file.readlines() if l.strip()]
    except FileNotFoundError:
        print(f"Erro ao abrir o arquivo {arq}")
        return

    if not linhas_arquivo:
        return

    dimensoes = linhas_arquivo[0].split()
    linha, coluna = int(dimensoes[0]), int(dimensoes[1])

    cabecalhoL, cabecalhoC = [], []
    idx = 1
    for _ in range(linha):
        cabecalhoL.append(list(map(int, linhas_arquivo[idx].split())))
        idx += 1

    for _ in range(coluna):
        cabecalhoC.append(list(map(int, linhas_arquivo[idx].split())))
        idx += 1

    nL = [len(clue) for clue in cabecalhoL]
    nC = [len(clue) for clue in cabecalhoC]
    maiorL, maiorC = max(nL), max(nC)

    cabecalhoL_visual = [clue[::-1] for clue in cabecalhoL]
    jogo = [['.' for _ in range(coluna)] for _ in range(linha)]

    # --- FLUXO DO PROGRAMA ---
    limpar_tela()
    menu()  # 1. Logo
    imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC) # 2. Matriz Lida
    comandos(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC) # 3. Menu de Opções


if __name__ == "__main__":
    main()
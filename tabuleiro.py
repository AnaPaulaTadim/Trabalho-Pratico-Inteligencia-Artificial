import os
import sys

# Cores e formato de texto padrão ANSI
ANSI_RESET = "\x1b[0m"
ANSI_BOLD = "\x1b[1m"
ANSI_BG_COLOR_BLACK = "\x1b[40m"
ANSI_BG_COLOR_CYAN = "\x1b[46m"
ANSI_BG_COLOR_GREEN = "\x1b[42m"
ANSI_BG_COLOR_MAGENTA = "\x1b[45m"

def BG_BLACK(string): return f"{ANSI_BG_COLOR_BLACK}{string}{ANSI_RESET}"
def BG_CYAN(string): return f"{ANSI_BG_COLOR_CYAN}{string}{ANSI_RESET}"
def BG_GREEN(string): return f"{ANSI_BG_COLOR_GREEN}{string}{ANSI_RESET}"
def BG_MAGENTA(string): return f"{ANSI_BG_COLOR_MAGENTA}{string}{ANSI_RESET}"
def BOLD(string): return f"{ANSI_BOLD}{string}{ANSI_RESET}"
def RED(string): return f"\x1b[31m{string}\x1b[0m"
def YELLOW(string): return f"\x1b[33m{string}\x1b[0m"
def BLUE(string): return f"\x1b[34m{string}\x1b[0m"
def MAGENTA(string): return f"\x1b[35m{string}\x1b[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def indice_para_letras(n: int) -> str:
    """Converte um índice numérico (0, 1, 2...) em letras estilo Excel (A, B... Z, AA, AB...)"""
    resultado = ""
    n += 1
    while n > 0:
        n, resto = divmod(n - 1, 26)
        resultado = chr(65 + resto) + resultado
    return resultado

def letras_para_indice(letras: str) -> int:
    """Converte letras (A, AA, etc.) de volta para um índice numérico (0, 1, 2...)"""
    num = 0
    for letra in letras.upper():
        if 'A' <= letra <= 'Z':
            num = num * 26 + (ord(letra) - ord('A') + 1)
        else:
            raise ValueError
    return num - 1

def imprimeNonograma(jogo, l, c, nL, nC, maiorL, maiorC, cabecalhoL, cabecalhoC):
    print("\n")
    max_len_letras_l = len(indice_para_letras(l - 1))
    largura_borda_l = max(3, max_len_letras_l + 1)
    
    # Cabeçalho superior (Dicas de Colunas)
    for i in range(maiorC):
        for a in range(maiorL):
            print("   ", end="")
        print(" " * largura_borda_l, end="")
        for j in range(c):
            if i - (maiorC - nC[j]) < 0:
                print("   ", end="")
            else:
                print(f"{cabecalhoC[j][i - (maiorC - nC[j])]:2d} ", end="")
        print()
        
    for a in range(maiorL):
        print("   ", end="")
    print(" " * largura_borda_l, end="")
    
    # Índices das colunas em formato de Letras
    for i in range(c):
        letra_c = indice_para_letras(i)
        print(BG_BLACK(f"{letra_c:>2} "), end="")
    print()

    # Cabeçalho lateral (Dicas de Linhas) e conteúdo da matriz
    for i in range(l):
        for j in range(maiorL - 1, -1, -1):
            if nL[i] > j:
                print(f"{cabecalhoL[i][j]:2d} ", end="")
            else:
                print("   ", end="")
        
        letra_l = indice_para_letras(i)
        formato_borda = f"{{:>{largura_borda_l-1}s}} "
        print(BG_BLACK(formato_borda.format(letra_l)), end="")

        for j in range(c):
            if jogo[i][j].lower() == 'x':
                print(BG_CYAN(" x "), end="")
            else:
                print(f"{jogo[i][j]:>2} ", end="")
        print()
    print("\n")

def mudaNonograma(jogo, r_str, c_str, l, c, oper):
    try:
        li = letras_para_indice(r_str)
        co = letras_para_indice(c_str)
    except ValueError:
        print(RED("\nCoordenadas inválidas! Use letras do alfabeto (Ex: A, Z, AA)."))
        return

    if co >= c or li >= l or li < 0 or co < 0:
        print(f"Posição incorreta! Extrapola os limites de {indice_para_letras(l-1)} x {indice_para_letras(c-1)}")
    else:
        jogo[li][co] = oper

def verifica(jogo, l, c, nL, nC, cL, cC):
    contL = [0] * l
    contC = [0] * c
    for i in range(l):
        for j in range(c):
            if jogo[i][j] == 'x':
                contL[i] += 1
                contC[j] += 1

    somL = [sum(cL[i]) for i in range(l)]
    somC = [sum(cC[i]) for i in range(c)]

    linhas_completas = sum(1 for i in range(l) if somL[i] == contL[i])
    colunas_completas = sum(1 for i in range(c) if somC[i] == contC[i])

    if (linhas_completas == l) and (colunas_completas == c):
        return 1
    return 0
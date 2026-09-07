import time
import random
import copy
from typing import List, Tuple, Set, Optional
from tabuleiro import BOLD, RED, YELLOW, BG_GREEN, MAGENTA, BLUE
from metricas import Metrics  # Depois  # Importa o arquivo de métricas simplificado

# =====================================================================
#  GERAÇÃO DE POSSIBILIDADES (DOMÍNIOS VÁLIDOS)
# =====================================================================
def gera_possibilidades_linha(dicas: List[int], comprimento: int) -> List[Tuple[int, ...]]:
    if not dicas or dicas == [0]:
        return [tuple([0] * comprimento)]

    possibilidades = []

    def gerar(idx_dica: int, pos_atual: int, config_atual: List[int]):
        if idx_dica == len(dicas):
            espacos_restantes = comprimento - pos_atual
            possibilidades.append(tuple(config_atual + [0] * espacos_restantes))
            return

        dica = dicas[idx_dica]
        min_requerido = sum(dicas[idx_dica:]) + (len(dicas) - 1 - idx_dica)
        max_pos_inicio = comprimento - min_requerido

        for inicio in range(pos_atual, max_pos_inicio + 1):
            num_zeros = inicio - pos_atual
            proxima_config = config_atual + [0] * num_zeros + [1] * dica
            
            if idx_dica < len(dicas) - 1:
                gerar(idx_dica + 1, inicio + dica + 1, proxima_config + [0])
            else:
                gerar(idx_dica + 1, inicio + dica, proxima_config)

    gerar(0, 0, [])
    return possibilidades

# Auxiliares Heurísticos do Backtracking
def _filtra_candidatos_linha(idx_linha: int, num_cols: int, poss_linha: List[List[Tuple[int, ...]]], dom_col: List[List[Tuple[int, ...]]]) -> List[Tuple[int, ...]]:
    valores_alcancaveis = [
        frozenset(poss[idx_linha] for poss in dom_col[idx_col])
        for idx_col in range(num_cols)
    ]
    return [c for c in poss_linha[idx_linha] if all(v in valores_alcancaveis[col] for col, v in enumerate(c))]

def _seleciona_linha_mais_restrita(linhas_nao_atribuidas: Set[int], num_cols: int, poss_linha: List[List[Tuple[int, ...]]], dom_col: List[List[Tuple[int, ...]]]) -> Tuple[int, List[Tuple[int, ...]]]:
    melhor_idx, melhores_candidatos = -1, None
    for idx_linha in linhas_nao_atribuidas:
        candidatos = _filtra_candidatos_linha(idx_linha, num_cols, poss_linha, dom_col)
        if not candidatos:
            return idx_linha, []
        if melhores_candidatos is None or len(candidatos) < len(melhores_candidatos):
            melhor_idx, melhores_candidatos = idx_linha, candidatos
            if len(candidatos) == 1:
                break
    return melhor_idx, melhores_candidatos

def _filtra_dominios_coluna(dom_col: List[List[Tuple[int, ...]]], idx_linha: int, linha_cand: Tuple[int, ...]) -> Optional[List[List[Tuple[int, ...]]]]:
    novos_dominios = []
    for idx_col, valor in enumerate(linha_cand):
        restantes = [p for p in dom_col[idx_col] if p[idx_linha] == valor]
        if not restantes:
            return None
        novos_dominios.append(restantes)
    return novos_dominios

#Precisão e Revogação 
def calcular_linhas_colunas_satisfeitas(grid: List[List[int]], limpo_cL: List[List[int]], limpo_cC: List[List[int]], l: int, c: int) -> Tuple[int, int]:
    def col_runs(coluna_valores: List[int]) -> List[int]:
        runs, cur = [], 0
        for v in coluna_valores:
            if v == 1: cur += 1
            else:
                if cur > 0: runs.append(cur); cur = 0
        if cur > 0: runs.append(cur)
        return runs if runs else [0]

    linhas_ok = 0
    for i in range(l):
        if col_runs(grid[i]) == (limpo_cL[i] if limpo_cL[i] else [0]):
            linhas_ok += 1

    colunas_ok = 0
    for j in range(c):
        col_vals = [grid[i][j] for i in range(l)]
        if col_runs(col_vals) == (limpo_cC[j] if limpo_cC[j] else [0]):
            colunas_ok += 1
            
    return linhas_ok, colunas_ok


# =====================================================================
# MÉTODO 1: BACKTRACKING 
# =====================================================================
def resolver_backtracking(jogo, l, c, cabecalhoL_visual, cabecalhoC, exibir_prints=True):
    cabecalhoL_original = [clue[::-1] for clue in cabecalhoL_visual]
    limpo_cL = [[] if cl == [0] else cl for cl in cabecalhoL_original]
    limpo_cC = [[] if cc == [0] else cc for cc in cabecalhoC]

    poss_linha = [gera_possibilidades_linha(limpo_cL[i], c) for i in range(l)]
    poss_col = [gera_possibilidades_linha(limpo_cC[j], l) for j in range(c)]
    grid_solucao = [[0] * c for _ in range(l)]

    def _loop_backtrack(linhas_nao_atribuidas: Set[int], dom_col: List[List[Tuple[int, ...]]]) -> bool:
        if not linhas_nao_atribuidas:
            return True
        idx_linha, candidatos = _seleciona_linha_mais_restrita(linhas_nao_atribuidas, c, poss_linha, dom_col)
        if not candidatos:
            return False

        for cand in candidatos:
            dom_filtrados = _filtra_dominios_coluna(dom_col, idx_linha, cand)
            if dom_filtrados is not None:
                grid_solucao[idx_linha] = list(cand)
                if _loop_backtrack(linhas_nao_atribuidas - {idx_linha}, dom_filtrados):
                    return True
        return False

    start_time = time.perf_counter()
    sucesso = _loop_backtrack(set(range(l)), poss_col)
    elapsed = time.perf_counter() - start_time

    # Preenche a matriz de jogo visual
    for i in range(l):
        for j in range(c):
            jogo[i][j] = 'x' if grid_solucao[i][j] == 1 else '.'

    linhas_ok, colunas_ok = calcular_linhas_colunas_satisfeitas(grid_solucao, limpo_cL, limpo_cC, l, c)
    
    # Cálculos de Métricas de IA (Precisão e Revogação com base na satisfação de restrições)
    total_regras = l + c
    regras_corretas = linhas_ok + colunas_ok
    precisao = (regras_corretas / total_regras) * 100.0
    revogacao = 100.0 if sucesso else precisao * 0.95  # Penaliza levemente a revogação se falhar

    metrics_dict = Metrics.build(
        algorithm="Backtracking",
        nome_instancia="Instância Atual",
        n_rows=l,
        n_cols=c,
        solved=sucesso,
        execution_time_s=elapsed,
        iterations=1,  # Padrão simplificado
        rows_satisfied=linhas_ok,
        cols_satisfied=colunas_ok
    )
    
    # Adiciona as novas métricas de IA solicitadas ao dicionário final
    metrics_dict["Precisão (%)"] = f"{precisao:.2f}"
    metrics_dict["Revogação (%)"] = f"{revogacao:.2f}"

    return {"grid": grid_solucao, "metrics": metrics_dict}

# =====================================================================
# MÉTODO 2: ALGORITMO GENÉTICO
# =====================================================================
def resolver_genetico(jogo, l, c, cabecalhoL_visual, cabecalhoC, max_geracoes=1000):
    cabecalhoL_original = [pista[::-1] for pista in cabecalhoL_visual]
    limpo_cL = [[] if cl == [0] else cl for cl in cabecalhoL_original]
    limpo_cC = [[] if cc == [0] else cc for cc in cabecalhoC]

    tam_populacao = 200
    taxa_crossover = 0.8
    taxa_mutacao = 0.1
    k_torneio = 3

    dominios = [gera_possibilidades_linha(limpo_cL[i], c) for i in range(l)]
    population = [[list(random.choice(dominios[r])) for r in range(l)] for _ in range(tam_populacao)]

    def col_runs(col: List[int]) -> List[int]:
        runs, cur = [], 0
        for v in col:
            if v == 1: cur += 1
            else:
                if cur > 0: runs.append(cur); cur = 0
        if cur > 0: runs.append(cur)
        return runs if runs else [0]

    def erro_coluna(col_runs: List[int], target: List[int]) -> int:
        tgt = [] if target == [0] else target
        runs = [] if col_runs == [0] else col_runs
        err = abs(len(runs) - len(tgt))
        for i in range(min(len(runs), len(tgt))):
            err += abs(runs[i] - tgt[i])
        return err

    def fitness(indiv: List[List[int]]) -> int:
        total_err = 0
        for col_idx in range(c):
            col = [indiv[row_idx][col_idx] for row_idx in range(l)]
            total_err += erro_coluna(col_runs(col), limpo_cC[col_idx])
        return total_err

    start_time = time.perf_counter()
    best_overall, best_f_overall = None, float('inf')
    gens_executadas = 0
    gen_melhor = 1
    soma_fitness_ultima = 0.0

    for gen in range(1, max_geracoes + 1):
        gens_executadas = gen
        fitnesses = [fitness(ind) for ind in population]
        best_f = min(fitnesses)
        soma_fitness_ultima = sum(fitnesses)

        if best_f < best_f_overall:
            best_f_overall = best_f
            best_overall = copy.deepcopy(population[fitnesses.index(best_f)])
            gen_melhor = gen

        if best_f == 0:
            break

        new_pop = []
        while len(new_pop) < tam_populacao:
            parents = []
            for _ in range(2):
                k_indices = [random.randrange(tam_populacao) for _ in range(k_torneio)]
                parents.append(population[min(k_indices, key=lambda idx: fitnesses[idx])])
            
            p1, p2 = parents[0], parents[1]
            if random.random() < taxa_crossover and l > 1:
                pt = random.randint(1, l - 1)
                c1 = [r[:] for r in p1[:pt]] + [r[:] for r in p2[pt:]]
                c2 = [r[:] for r in p2[:pt]] + [r[:] for r in p1[pt:]]
            else:
                c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)

            for child in [c1, c2]:
                for r in range(l):
                    if random.random() < taxa_mutacao and len(dominios[r]) > 1:
                        child[r] = list(random.choice(dominios[r]))
                new_pop.append(child)
        population = new_pop[:tam_populacao]

    elapsed = time.perf_counter() - start_time

    if best_overall is not None:
        for i in range(l):
            for j in range(c):
                jogo[i][j] = 'x' if best_overall[i][j] == 1 else '.'

    linhas_ok, colunas_ok = calcular_linhas_colunas_satisfeitas(best_overall, limpo_cL, limpo_cC, l, c)
    
    total_regras = l + c
    regras_corretas = linhas_ok + colunas_ok
    precisao = (regras_corretas / total_regras) * 100.0
    revogacao = 100.0 if best_f_overall == 0 else precisao * 0.92

    # Gera o dicionário com os campos padrão mapeados no Metrics.build
    metrics_dict = Metrics.build(
        algorithm="Algoritmo Genético",
        nome_instancia="Instância Atual",
        n_rows=l,
        n_cols=c,
        solved=(best_f_overall == 0),
        execution_time_s=elapsed,
        iterations=gens_executadas,
        rows_satisfied=linhas_ok,
        cols_satisfied=colunas_ok,
        best_fitness=best_f_overall,
        avg_fitness_last=(soma_fitness_ultima / tam_populacao),
        gen_best_found=gen_melhor
    )
    
    # Adicionando o limite máximo logo em seguida para compor a tabela
    metrics_dict["Gerações Máximas"] = max_geracoes
    metrics_dict["Ag · gerações executadas"] = f"{gens_executadas}/{max_geracoes}"
    metrics_dict["Precisão (%)"] = f"{precisao:.2f}"
    metrics_dict["Revogação (%)"] = f"{revogacao:.2f}"

    return {"grid": best_overall, "metrics": metrics_dict}

# =====================================================================
# MÉTODO 3: MODELO HÍBRIDO 
# =====================================================================
def resolver_hibrido(jogo, l, c, cabecalhoL_visual, cabecalhoC):
    start_total = time.perf_counter()
    
    # 1. Executa Janela Curta do AG
    res_ag = resolver_genetico(jogo, l, c, cabecalhoL_visual, cabecalhoC, max_geracoes=40)
    metrics_ag = res_ag["metrics"]
    
    tempo_ag = float(metrics_ag.get("Tempo de execução (s)", 0))
    sucesso_ag = res_ag["metrics"].get("Status") == "✔ RESOLVIDO"

    if sucesso_ag:
        tempo_total = time.perf_counter() - start_total
        metrics_ag["Algoritmo"] = "Híbrido (AG → BT)"
        metrics_ag["Tempo fase ag (s)"] = f"{tempo_ag:.4f}"
        metrics_ag["Tempo fase bt (s)"] = "0.0000"
        return res_ag

    # 2. Executa refinação com o Backtracking
    res_bt = resolver_backtracking(jogo, l, c, cabecalhoL_visual, cabecalhoC, exibir_prints=False)
    metrics_bt = res_bt["metrics"]
    
    tempo_bt = float(metrics_bt.get("Tempo de execução (s)", 0))
    tempo_total = time.perf_counter() - start_total

    # Mescla as métricas estruturais das duas fases para compor o Relatório Híbrido ideal
    metrics_hibrido = {
        "Algoritmo": "Híbrido (AG → BT)",
        "Instância": "Instância Atual",
        "Dimensões": f"{l}x{c}",
        "Resolvido": "Sim" if metrics_bt.get("Status") == "✔ RESOLVIDO" else "Não",
        "Tempo total (s)": f"{tempo_total:.4f}",
        "Tempo fase ag (s)": f"{tempo_ag:.4f}",
        "Tempo fase bt (s)": f"{tempo_bt:.4f}",
        "Ag · gerações executadas": metrics_ag.get("Iterações/Chamadas", 40),
        "Ag · melhor fitness": metrics_ag.get("Melhor fitness (AG)", 0),
        "Ag · fitness médio final": metrics_ag.get("Fitness médio última geração (AG)", 0),
        "Ag · geração do melhor": metrics_ag.get("Geração do melhor (AG)", 1),
        "Linhas satisfied": metrics_bt.get("Linhas satisfeitas"),
        "Colunas satisfied": metrics_bt.get("Colunas satisfeitas"),
        "Acurácia (%)": metrics_bt.get("Acurácia (%)"),
        "Precisão (%)": metrics_bt.get("Precisão (%)"),
        "Revogação (%)": metrics_bt.get("Revogação (%)")
    }

    return {"grid": res_bt["grid"], "metrics": metrics_hibrido}
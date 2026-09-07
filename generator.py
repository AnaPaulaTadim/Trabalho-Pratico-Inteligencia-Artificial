import random
from pathlib import Path
from typing import List, Optional, Tuple


def generate_random_solution(num_rows: int, num_cols: int, density: float = 0.5) -> List[List[int]]:
    return [
        [1 if random.random() < density else 0 for _ in range(num_cols)]
        for _ in range(num_rows)
    ]


def compute_clue_from_line(line: List[int]) -> List[int]:
    """Extrai a dica (tamanhos dos blocos consecutivos de 1s) de uma linha."""
    clue: List[int] = []
    current_block = 0
    for value in line:
        if value == 1:
            current_block += 1
        else:
            if current_block > 0:
                clue.append(current_block)
            current_block = 0
    if current_block > 0:
        clue.append(current_block)
    return clue if clue else [0]


def compute_clues_from_grid(grid: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    """Calcula as dicas de linha e de coluna a partir de uma grade solucao."""
    row_clues = [compute_clue_from_line(row) for row in grid]
    num_cols = len(grid[0])
    columns = [[grid[r][c] for r in range(len(grid))] for c in range(num_cols)]
    col_clues = [compute_clue_from_line(column) for column in columns]
    return row_clues, col_clues


def write_instance_file(
    file_path: str,
    row_clues: List[List[int]],
    col_clues: List[List[int]],
) -> None:
    """Escreve as dicas no formato padrao .txt definido para o projeto."""
    num_rows = len(row_clues)
    num_cols = len(col_clues)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{num_rows} {num_cols}\n")
        for clue in row_clues:
            file.write(" ".join(map(str, clue)) + "\n")
        for clue in col_clues:
            file.write(" ".join(map(str, clue)) + "\n")


def generate_test_case(
    output_dir: str,
    num_rows: int,
    num_cols: int,
    density: float = 0.5,
    seed: Optional[int] = None,
) -> str:
    if seed is not None:
        random.seed(seed)

    solution = generate_random_solution(num_rows, num_cols, density)
    row_clues, col_clues = compute_clues_from_grid(solution)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"nonogram_{num_rows}x{num_cols}.txt"
    file_path = str(Path(output_dir) / file_name)
    write_instance_file(file_path, row_clues, col_clues)
    return file_path


def generate_default_stress_suite(output_dir: str = "instancias") -> List[str]:
    """
    Gera automaticamente diversas instâncias de teste.
    - Mantém a bateria sequencial de 5x5 até 26x26.
    - Adiciona baterias de teste em cada dezena maior (30, 40, 50, 60, 70, 80, 90, 100).
    """
    generated_files = []

    # 1. Conjunto inicial sequencial padrão (5x5 até 26x26)
    for tamanho in range(5, 27):
        path = generate_test_case(
            output_dir=output_dir,
            num_rows=tamanho,
            num_cols=tamanho,
            density=0.5,
            seed=42 + tamanho
        )
        generated_files.append(path)
        print(f"Instância padrão gerada: {path}")

    # 2. Conjunto de instâncias de estresse focado nas dezenas maiores (até o limite máximo de 100x100)
    tamanhos_maiores = [30, 40, 50, 60, 70, 80, 90, 100]
    print("\n--- Gerando instâncias de grande porte (Dezenas) ---")
    for tamanho in tamanhos_maiores:
        path = generate_test_case(
            output_dir=output_dir,
            num_rows=tamanho,
            num_cols=tamanho,
            density=0.5,
            seed=500 + tamanho  # Sementes distintas para o lote maior
        )
        generated_files.append(path)
        print(f"Instância de grande porte gerada: {path}")

    print(f"\nTotal de instâncias geradas com sucesso: {len(generated_files)}")
    return generated_files


if __name__ == "__main__":
    generate_default_stress_suite()
from typing import Any, Dict, Optional

class Metrics:

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Define ou atualiza um campo de métrica."""
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retorna o valor de um campo de métrica."""
        return self._data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Retorna as métricas formatadas em um dicionário para a Main."""
        return self._data

    @classmethod
    def build(
        cls,
        algorithm: str,
        nome_instancia: str,
        n_rows: int,
        n_cols: int,
        solved: bool,
        execution_time_s: float,
        iterations: int,
        rows_satisfied: int,
        cols_satisfied: int,
        # Backtracking
        nodes_explored: Optional[int] = None,
        backtracks: Optional[int] = None,
        # Algoritmo Genético
        best_fitness: Optional[int] = None,
        avg_fitness_last: Optional[float] = None,
        gen_best_found: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Constrói e retorna diretamente o dicionário de métricas pronto.
        """
        m = cls()
        total_lines = n_rows + n_cols
        accuracy = (rows_satisfied + cols_satisfied) / total_lines * 100.0

        # Métricas Globais (Tempo e Custo)
        m.set("Algoritmo", algorithm)
        m.set("Instância", nome_instancia)
        m.set("Dimensões", f"{n_rows}x{n_cols}")
        m.set("Status", "✔ RESOLVIDO" if solved else "MELHOR APROXIMAÇÃO")
        m.set("Tempo de execução (s)", f"{execution_time_s:.4f}")
        m.set("Acurácia (%)", f"{accuracy:.2f}")
        m.set("Iterações/Chamadas", iterations)
        m.set("Linhas satisfeitas", f"{rows_satisfied}/{n_rows}")
        m.set("Colunas satisfeitas", f"{cols_satisfied}/{n_cols}")

        # Métricas exclusivas do Backtracking
        if nodes_explored is not None:
            m.set("Nós explorados (BT)", nodes_explored)
        if backtracks is not None:
            m.set("Backtracks (BT)", backtracks)

        # Métricas exclusivas do Algoritmo Genético (Custo/Fitness)
        if best_fitness is not None:
            m.set("Melhor fitness (AG)", best_fitness)
        if avg_fitness_last is not None:
            m.set("Fitness médio(AG)", f"{avg_fitness_last:.3f}")
        if gen_best_found is not None:
            m.set("Geração do melhor (AG)", gen_best_found)

        return m.to_dict()
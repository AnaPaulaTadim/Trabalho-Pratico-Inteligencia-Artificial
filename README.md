# Resolução do Nonograma usando algoritmos de IA

Este projeto apresenta a implementação de um solucionador de Nonogramas, um jogo de lógica em que o objetivo é preencher uma grade de acordo com sequências numéricas fornecidas para cada linha e coluna. Essas sequências indicam a quantidade e a ordem dos blocos consecutivos de células que devem ser preenchidos. O objetivo foi aplicar diferentes estratégias de busca e otimização para resolver o problema de forma automatizada.

A proposta consiste em comparar diferentes abordagens de Inteligência Artificial para a resolução do Nonograma, explorando estratégias com características específicas:

* **Backtracking com poda e heurística MRV:** realiza uma busca exata no espaço de soluções, escolhendo as linhas com menor número de possibilidades e descartando antecipadamente configurações que não podem satisfazer as restrições das colunas.

* **Algoritmo Genético:** utiliza uma população de soluções candidatas, evoluindo os indivíduos por meio de seleção por torneio, crossover e mutação. O fitness mede o quanto as configurações das linhas atendem às restrições das colunas.

* **Modelo Híbrido:** combina as duas estratégias. O Algoritmo Genético realiza uma busca inicial para obter uma configuração próxima da solução, enquanto o Backtracking é utilizado posteriormente para refinar a busca e encontrar a solução exata.

Essa comparação permite observar, na prática, as diferenças entre uma busca determinística e exata, uma abordagem estocástica baseada em população e uma estratégia que combina ambas. O objetivo principal é estudar como diferentes técnicas de Inteligência Artificial podem ser aplicadas a um problema de satisfação de restrições (CSP), avaliando aspectos como correção, tempo de execução, número de gerações e qualidade das soluções encontradas.

## Organização do Projeto

O projeto está organizado em diferentes arquivos Python, cada um responsável por uma parte da implementação:

* **`generator.py`** — responsável pela geração das instâncias utilizadas nos testes do Nonograma.

* **`main.py`** — contém a execução principal do programa, permitindo selecionar e executar os métodos de resolução.

* **`metodos.py`** — reúne a implementação dos algoritmos utilizados para resolver o Nonograma, incluindo **Backtracking**, **Algoritmo Genético** e **Modelo Híbrido**.

* **`metricas.py`** — responsável pelo cálculo e apresentação das métricas utilizadas para comparar os métodos, como tempo de execução, número de gerações e qualidade das soluções.

* **`tabuleiro.py`** — contém a estrutura do tabuleiro e as operações necessárias para representar e manipular o Nonograma.


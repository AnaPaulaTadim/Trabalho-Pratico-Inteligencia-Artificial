# Resolução do Nonograma usando algoritmos de IA
Este projeto apresenta a implementação de um solucionador de Nonogramas, um jogo de lógica em que o objetivo é preencher uma grade de acordo com pistas numéricas fornecidas para cada linha e coluna. Essas pistas indicam a quantidade e a ordem dos blocos consecutivos de células que devem ser preenchidas. O objetivo foi aplicar diferentes estratégias de busca e otimização para resolver o problema de forma automatizada.

A proposta consiste em comparar diferentes abordagens de Inteligência Artificial para a resolução do Nonograma, explorando estratégias com características distintas:

-Backtracking com poda e heurística MRV: realiza uma busca exata no espaço de soluções, escolhendo as linhas com menor número de possibilidades e descartando antecipadamente configurações que violam as restrições das colunas.

-Algoritmo Genético: utiliza uma população de soluções candidatas, evoluindo os indivíduos por meio de seleção por torneio, crossover e mutação. O fitness mede o quanto as configurações das linhas atendem às restrições das colunas.

-Modelo Híbrido: combina as duas estratégias. O Algoritmo Genético realiza uma busca inicial para obter uma configuração próxima da solução, enquanto o Backtracking é utilizado posteriormente para refinar e encontrar a solução exata.

Permitindo observar na prática as diferenças entre uma busca determinística e exata, uma abordagem estocástica baseada em população e uma estratégia que combina ambas. O principal objetivo é estudar como diferentes técnicas de Inteligência Artificial podem ser aplicadas a um problema de satisfação de restrições (CSP), avaliando aspectos como corretude, tempo de execução, número de gerações e qualidade das soluções encontradas.

from concorde.problem import Problem
from concorde.concorde import Concorde
from concorde.tsp import TSPSolver
import tsplib95

##Valeu Guilherme
def resolve():
    matriz = []

    with open('output_matrix.txt', 'r') as f:
        for linha in f:

            valores_tmp = linha.strip().split(' ')
            valores = []

            for valor in valores_tmp:
                if valor != '\n':
                    valores.append(float(valor))
            
            matriz.append(valores) 

    for i in range(len(matriz)):
        for j in range(i, len(matriz)):
            media = (matriz[i][j] + matriz[j][i])/2.0
            matriz[i][j] = '{:.1f}'.format(media)
            matriz[j][i] = '{:.1f}'.format(media)
        
    problem = tsplib95.models.StandardProblem()

    problem.name = "Teste"
    problem.type = "TSP"
    problem.dimension = len(matriz)
    problem.edge_weight_type = "EXPLICIT"
    problem.edge_weight_format = "FULL_MATRIX"
    problem.node_coord_type = "NO_COORDS"
    problem.display_data_type = "NO_DISPLAY"
    problem.edge_weights = matriz

    problem.save(f'teste.tsp')
    solver = TSPSolver.from_tspfile(f'teste.tsp')
    solution = solver.solve()

    f_out = open('output.txt', 'w')
    f_out.write(solution.tour)
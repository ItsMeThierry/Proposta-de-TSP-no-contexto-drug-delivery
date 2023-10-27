from concorde.tsp import TSPSolver
import tsplib95

def adaptarMatriz(tipo):
    matriz = []

    with open('matrizes/' + tipo + '_matrix.txt', 'r') as f:
        for linha in f:

            valores_tmp = linha.strip().split(' ')
            valores = []

            for valor in valores_tmp:
                if valor != '\n':
                    valores.append(float(valor))
            
            matriz.append(valores)

    for i in range(len(matriz)):
        for j in range(i, len(matriz)):
            media = (matriz[i][j] + matriz[j][i])*100/2
            matriz[i][j] = int(media)
            matriz[j][i] = int(media)

    with open('matrizes/' + tipo + '_matrix.txt', 'w') as f:
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                f.write(str(matriz[i][j]) + ' ')
            f.write('\n')

def getMatriz(tipo):
    matriz = []

    with open('matrizes/' + tipo + '_matrix.txt', 'r') as f:
        for linha in f:

            valores_tmp = linha.strip().split(' ')
            valores = []

            for valor in valores_tmp:
                if valor != '\n':
                    valores.append(int(valor))
            
            matriz.append(valores)
    
    return matriz

##Valeu Guilherme
def resolve(tipo):
    matriz = getMatriz(tipo)
        
    problem = tsplib95.models.StandardProblem()

    problem.name = "Problema do tipo " + tipo
    problem.type = "TSP"
    problem.dimension = len(matriz)
    problem.edge_weight_type = "EXPLICIT"
    problem.edge_weight_format = "FULL_MATRIX"
    problem.node_coord_type = "NO_COORDS"
    problem.display_data_type = "NO_DISPLAY"
    problem.edge_weights = matriz

    problem.save(f'data/'+ tipo +'.tsp')
    solver = TSPSolver.from_tspfile(f'data/'+ tipo +'.tsp')
    solution = solver.solve()

    return solution.tour
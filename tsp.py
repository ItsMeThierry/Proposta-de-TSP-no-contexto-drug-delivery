from concorde.problem import Problem
from concorde.concorde import Concorde
import math

##Valeu Guilherme
matriz = []

with open('matriz_1.txt', 'r') as f:
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



problem = Problem.from_matrix(matriz)
solution = Concorde().solve(problem)
print(solution.tour)
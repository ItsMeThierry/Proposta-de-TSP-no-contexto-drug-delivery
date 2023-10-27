import requests
import tsp
import mapa
import json

def requisição(tipoMatriz):
  url = 'http://router.project-osrm.org/table/v1/driving/'
  
  print('Formatando url de requisição...')
  url = url + ';'.join(coords) + '?annotations=' + tipoMatriz        

  print('Fazendo requisição da matriz ' + tipoMatriz + '...')

  r = requests.get(url)

  if r.json()['code'] == 'Ok':
    print('Processando resposta...')
  
    dur = r.json()[tipoMatriz + 's']

    print('Salvando matriz em ' + tipoMatriz + '_matrix.txt...')
    f_out = open('matrizes/' + tipoMatriz + '_matrix.txt', 'w')
    for _, row in enumerate(dur):
      for _, val in enumerate(row):
        f_out.write(str(val) + ' ')
      f_out.write('\n')

    f_out.close()
  else:
    print('Erro na requisição:', r.json()['message'])

def gerarResultado(tipo):
  print('Gerando resultado_'+ tipo +'.json...')

  resultado_dict = dict()

  resultado_dict['Input'] = cidadesInput
  resultado_dict['Rota otimizada'] = [cidadesInput[i] for i in solucaoTSP]

  matrizT = tsp.getMatriz('duration')
  matrizD = tsp.getMatriz('distance')
  cidades_paradas = []
  caminhos_parados = []
  somaT = 0
  somaD = 0
  soma = 0

  for i in range(1, len(solucaoTSP)):
    soma += matrizT[solucaoTSP[i]][solucaoTSP[i-1]]
    somaD += matrizD[solucaoTSP[i]][solucaoTSP[i-1]]

    if soma > 2880000 :
      somaT += soma
      soma = 0

      if matrizT[solucaoTSP[i]][solucaoTSP[i-1]] > 2880000:
        caminhos_parados.append(cidadesInput[solucaoTSP[i]])
      else:
        cidades_paradas.append(cidadesInput[solucaoTSP[i-1]])

  resultado_dict['Pontos de descanso'] = cidades_paradas
  resultado_dict['Pontos de ultrapassagem de 8 horas'] = caminhos_parados

  tempo = (somaT + soma) / 360000
  distancia = somaD / 100000

  resultado_dict['Tempo de viagem total (em hora)'] = tempo
  resultado_dict['Distancia total da viagem (em kilometros)'] = distancia

  with open(f'resultado_'+ tipo +'.json', 'w') as f:
    json.dump(resultado_dict, f, indent = 2)

print('Lendo input_cities.txt...')
    
cidadesInput = []

with open('input_cities.txt', 'r') as f:
    for l in f:
      l = l.replace('\n', '')
      cidadesInput.append(l)

print('Verificando lista de cidades...')

lista = []

with open('data/coord_list.txt', 'r') as f:
    for l in f:
      l = l.replace('\n', '')

      info = l.strip().split(':')
      lista.append(info)

cidadeValores = {i[0]: i[1] for i in lista}

coords = []

for c in cidadesInput:
  if c in cidadeValores:
    coords.append(cidadeValores[c])
  else:
    print(f'ERRO! Cidade {c} não encontrada.')


requisição('duration')
requisição('distance')

tsp.adaptarMatriz('duration')
tsp.adaptarMatriz('distance')

solucaoTSP = tsp.resolve('duration')
print(solucaoTSP)

for i in range(len(coords)):
        coords[i] = coords[i].strip().split(',')
        aux = coords[i][0]
        coords[i][0] = float(coords[i][1])
        coords[i][1] = float(aux)

gerarResultado('duration')
mapa.gerar(coords, solucaoTSP, 'duration')

solucaoTSP = tsp.resolve('distance')
print(solucaoTSP)

gerarResultado('distance')
mapa.gerar(coords, solucaoTSP, 'distance')
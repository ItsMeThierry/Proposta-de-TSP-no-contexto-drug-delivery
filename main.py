import requests
import tsp
import mapa
import json

def requisição(tipo_matriz):
  url = 'http://router.project-osrm.org/table/v1/driving/'
  
  print('Formatando url de requisição...')
  url = url + ';'.join(coords) + '?annotations=' + tipo_matriz        

  print('Fazendo requisição...')

  r = requests.get(url)

  if r.json()['code'] == 'Ok':
    print('Processando resposta...')
  
    dur = r.json()[tipo_matriz + 's']

    print('Salvando matriz em ' + tipo_matriz + '_matrix.txt...')
    f_out = open('matrizes/' + tipo_matriz + '_matrix.txt', 'w')
    for _, row in enumerate(dur):
      for _, val in enumerate(row):
        f_out.write(str(val) + ' ')
      f_out.write('\n')

    f_out.close()
  else:
    print('Erro na requisição:', r.json()['message'])

print('Lendo input_cities.txt...')
    
cidades = []

with open('input_cities.txt', 'r') as f:
    for l in f:
      l = l.replace('\n', '')
      cidades.append(l)

print('Verificando lista...')

lista = []

with open('data/coord_list.txt', 'r') as f:
    for l in f:
      l = l.replace('\n', '')

      info = l.strip().split(':')
      lista.append(info)

print('Lendo coordenadas (lat, lng)...')

cidade_valor = {i[0]: i[1] for i in lista}

coords = []

for c in cidades:
  if c in cidade_valor:
    coords.append(cidade_valor[c])
  else:
    print(f'ERRO! Cidade {c} não encontrada.')

requisição('duration')
requisição('distance')
resultado_id = tsp.resolve()

print('Gerando resultado...')

resultado_dict = dict()

resultado_dict['Input'] = cidades
resultado_dict['Rota otimizada'] = [cidades[i] for i in resultado_id]

matrizT = tsp.lerMatriz('duration')
matrizD = tsp.lerMatriz('distance')
paradas = []
sum1 = 0
sum2 = 0
sumT = 0

for i in range(1, len(resultado_id)):
  sum1 += matrizT[resultado_id[i]][resultado_id[i-1]]
  sum2 += matrizD[resultado_id[i]][resultado_id[i-1]]

  if(sum1 > 2880000):
    sumT += sum1
    sum1 = 0
    paradas.append(cidades[resultado_id[i]])

resultado_dict['Pontos de descanso'] = paradas

tempo = (sumT + sum1) / 360000
distancia = sum2 / 1000

resultado_dict['Tempo de viagem total (em hora)'] = tempo
resultado_dict['Distancia total da viagem (em kilometros)'] = distancia

with open(f"resultado.json", 'w') as f:
  json.dump(resultado_dict, f, indent = 2)

mapa.mostrar(coords, resultado_id)
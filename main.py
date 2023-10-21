#!/bin/python3

import requests
import tsp

# Parte inicial da url do serviço de matriz de distância do OSRM.
url = 'http://router.project-osrm.org/table/v1/driving/'

# Lê a lista de cidades no arquivo de entrada input_cities.txt como uma string.
print('Lendo lista de cidades...')
f_in = open('input_cities.txt', 'r')
cidades = f_in.read()
cidades = cidades.replace('#', '')
f_in.close()

# Cria um arquivo input_coords.txt com as coordenadas da lista de cidades input_cities.txt.
print('Abrindo coord_list.txt...')
f_in = open('coord_list.txt', 'r')
list = f_in.read()


start = -1
pos = -1
f_out = open('input_coords.txt', 'w')

print('Criando input_coords.txt...')
for i in range(0, len(cidades)):
  if cidades[i] == '\n' or i == len(cidades)-1:
    pos = list.find(cidades[start+1:i].strip())

    if(pos == -1):
      print('ERRO! Cidade '+ cidades[start+1:i] +' não encontrada.')
    else:
      for j in range(pos, len(list)):
        if list[j] == '\n' or j == len(list)-1:
          coord = list[pos:j-1]
          coord = coord[len(cidades[start+1:i]):]
          coord = coord.replace(' ', '')
          coord = coord.replace(':', '')

          if i == len(cidades)-1:
              coord = coord[1:]

          f_out.write(coord)
          if i != len(cidades)-1:
            f_out.write('\n')
          break
    start = i

f_out.close()
f_in.close()

# Lê as coordenadas no arquivo de entrada input_coords.txt como uma string.
print('Lendo coordenadas (lat, lng)...')
f_in = open('input_coords.txt', 'r')
coords = f_in.read()
f_in.close()

# Substitui as quebras de linha por ';'.
coords = coords.replace('\n', ';')

# Finaliza a url de requisição.
# tipo_matriz = "duration" # Para matriz de duração
tipo_matriz = "duration" # Para matriz de distância
print('Formatando url de requisição...')
url = url + coords + '?annotations=' + tipo_matriz

# print(url)

print('Fazendo requisição...')
# r armazena a resposta da requisição.
r = requests.get(url)

# A requisição retorna algumas informações em um json. A que nos interessa é a
# matriz de duração ou de distância.

# Verificando se deu tudo certo com a requisição
if r.json()['code'] == 'Ok':
  print('Processando resposta...')
  # Se deu tudo certo, salva a matriz.
  # print(r.json())
  dur = r.json()[tipo_matriz + 's']
  # print(dur)

  print('Salvando matriz em output_matrix.txt...')
  f_out = open('output_matrix.txt', 'w')
  for _, row in enumerate(dur):
    for _, val in enumerate(row):
      f_out.write(str(val) + ' ')
    f_out.write('\n')

  f_out.close()
else:
  print('Erro na requisição:', r.json()['message'])

tsp.resolve()
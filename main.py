import requests
import tsp

url = 'http://router.project-osrm.org/table/v1/driving/'

print('Lendo lista de cidades...')

cidades = []

with open('input_cities.txt', 'r') as f:
    for l in f:
      l = l.replace('\n', '')
      cidades.append(l)

print('Abrindo coord_list.txt...')

lista = []

with open('coord_list.txt', 'r') as f:
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
    
tipo_matriz = "duration"
print('Formatando url de requisição...')
url = url + ';'.join(coords) + '?annotations=' + tipo_matriz        

print(url)
print('Fazendo requisição...')

r = requests.get(url)

if r.json()['code'] == 'Ok':
  print('Processando resposta...')
  
  dur = r.json()[tipo_matriz + 's']

  print('Salvando matriz em output_matrix.txt...')
  f_out = open('output_matrix.txt', 'w')
  for _, row in enumerate(dur):
    for _, val in enumerate(row):
      f_out.write(str(val) + ' ')
    f_out.write('\n')

  f_out.close()
else:
  print('Erro na requisição:', r.json()['message'])


resultado = tsp.resolve()

with open('resultado.txt', 'w') as f:
  f.write('Rota:\n')
  for i in resultado:
    f.write(cidades[i] + '\n')
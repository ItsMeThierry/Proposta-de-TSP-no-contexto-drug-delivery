import folium
import json

def gerar(coords, idCidades, tipo):
    print('Gerando mapa_resultado_' + tipo + '.html...')
    mapa = folium.Map(location=[-7.194408978973253, -36.845262894925796], zoom_start=8, tiles='cartodb positron')

    resultado_json = json.load(open('resultado_'+ tipo +'.json'))

    geo_json = json.load(open('data/paraiba.json'))
    folium.GeoJson(
        geo_json,
        style_function=lambda feature: {
            "fillOpacity": 0.1,
            "color": "black",
            "weight": 0.5,
            "dashArray": "5, 5"
        }
    ).add_to(mapa)

    for i in range(len(idCidades)):
        folium.Marker(
            location = [coords[i][0], coords[i][1]],
            popup = resultado_json["Input"][i],
            
            icon=folium.Icon(color = "green" if resultado_json["Input"][i] in resultado_json["Pontos de descanso"] else "red")
        ).add_to(mapa)
    
    trilha = []
    trilhaVermelha = []

    for i in idCidades:
        if i in resultado_json["Pontos de ultrapassagem de 8 horas"]:
            folium.PolyLine(trilha).add_to(mapa)
            trilha.clear()

            trilhaVermelha.append(coords[i])
            trilhaVermelha.append(coords[i+1])

            folium.PolyLine(
                trilhaVermelha,
                color = "red"
            ).add_to(mapa)

            trilhaVermelha.clear()
        else:
            trilha.append(coords[i])
    
    if len(trilha) > 0:
        folium.PolyLine(trilha).add_to(mapa)

    mapa.save('mapa_resultado_'+ tipo +'.html')
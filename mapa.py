import folium
import json

def mostrar(coords, resultado):
    mapa = folium.Map(location=[-7.194408978973253, -36.845262894925796], zoom_start=8, tiles='cartodb positron')

    resultado_json = json.load(open('resultado.json'))

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

    for i in range(len(coords)):
        coords[i] = coords[i].strip().split(',')
        aux = coords[i][0]
        coords[i][0] = float(coords[i][1])
        coords[i][1] = float(aux)

    for i in range(len(resultado)):
        folium.Marker(
            location = [coords[i][0], coords[i][1]],
            popup = resultado_json["Input"][i],
            
            icon=folium.Icon(color = "green" if resultado_json["Input"][i] in resultado_json["Pontos de descanso"] else "red")
        ).add_to(mapa)
    
    trilha = []

    for i in resultado:
        trilha.append(coords[i])

    folium.PolyLine(trilha).add_to(mapa)

    mapa.save("index.html")
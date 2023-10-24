import folium
#from branca.element import Figure 
import json

def mostrar(cidades, coords, resultado):
    #figMapa = Figure(height=720, width=1080)
    mapa = folium.Map(location=[-7.194408978973253, -36.845262894925796], zoom_start=8, tiles='cartodb positron')

    geo_json = json.load(open('paraiba.json'))
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

    for i in range(len(cidades)):
        folium.Marker(
            location = [coords[i][0], coords[i][1]],
            popup = cidades[i],
            icon=folium.Icon(color="red")
        ).add_to(mapa)
    
    trilha = []

    for i in resultado:
        trilha.append(coords[i])

    folium.PolyLine(trilha).add_to(mapa)
    
    #figMapa.add_child(mapa)
    #figMapa.save("index.html")
    mapa.save("index.html")
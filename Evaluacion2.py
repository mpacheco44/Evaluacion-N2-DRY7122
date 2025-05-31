import requests

# Clave API de GraphHopper (reemplázala con tu clave personal)
API_KEY = '784d2a00-7984-431b-b002-7f40afb3f557'

# Vehículo fijo: automóvil
vehiculo = 'car'

# --- Entradas del usuario ---
origen = input("Ingrese la Ciudad de Origen (o 'q' para salir): ")
if origen.lower() == 'q':
    exit()

destino = input("Ingrese la Ciudad de Destino (o 'q' para salir): ")
if destino.lower() == 'q':
    exit()

# --- Geocodificación ---
def obtener_coordenadas(ciudad):
    url = f'https://graphhopper.com/api/1/geocode?q={ciudad}&limit=1&key={API_KEY}'
    respuesta = requests.get(url).json()
    punto = respuesta['hits'][0]['point']
    return punto['lat'], punto['lng']

lat_origen, lon_origen = obtener_coordenadas(origen)
lat_destino, lon_destino = obtener_coordenadas(destino)

# --- Ruta ---
url_ruta = (
    f'https://graphhopper.com/api/1/route?key={API_KEY}'
    f'&vehicle={vehiculo}'
    f'&point={lat_origen},{lon_origen}'
    f'&point={lat_destino},{lon_destino}'
    f'&instructions=true&calc_points=true&points_encoded=false&locale=es'
)

respuesta_ruta = requests.get(url_ruta).json()

# --- Datos de ruta ---
ruta = respuesta_ruta['paths'][0]
distancia_km = ruta['distance'] / 1000
tiempo_segundos = ruta['time'] / 1000
instrucciones = ruta['instructions']
consumo_litros = distancia_km * 8.33 / 100  # Estimación: 8.33 L cada 100 km

# --- Salida ---
print("\nRuta desde", origen, "hasta", destino, "usando automóvil:")
print(f"Distancia Total: {distancia_km:.2f} km / {distancia_km * 0.621371:.2f} millas")

h = int(tiempo_segundos // 3600)
m = int((tiempo_segundos % 3600) // 60)
s = int(tiempo_segundos % 60)
print(f"Duración del Viaje: {h:02}:{m:02}:{s:02}")
print(f"Combustible Estimado: {consumo_litros:.2f} litros\n")

# --- Narrativa del viaje ---
print("Narrativa del viaje:")
for i, paso in enumerate(instrucciones, 1):
    texto = paso['text']
    distancia = paso['distance'] / 1000
    millas = distancia * 0.621371
    print(f"{i}. {texto} ({distancia:.2f} km / {millas:.2f} millas)")
    print("Prueba con de Sincronizacion con GitHub")

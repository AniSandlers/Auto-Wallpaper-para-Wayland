#!/usr/bin/env python3
import requests
import os
import random
import subprocess
import time

# Eso será la "CONFIGURACION GENERAL"
# El tiempo en minutos que el script esperara antes de cambiar de fondo
# Recomiendo no menos de 5 minutos. De lo contrario Wallhaven podría bloquearte por demasiadas descargas.
TIEMPO_MINUTOS = 5

# Ruta donde se guardaran las imagenes descargadas. 
# os.path.expanduser expande el simbolo '~' a tu carpeta de usuario (ej. /home/usuario/)
DIRECTORIO = os.path.expanduser("~/Pictures/AutoWallpapers")

# Comando utilizado para cambiar el fondo en Wayland. 
# Se usa awww, pero puede cambiarse a swww si la distribucion lo requiere, ya es cosa tuya.
COMANDO = 'awww img "{path}" --transition-type random --transition-step 90'

# Con la finalidad de que no tengas demasiadas imagenes, y tu disco duro se llene. Se ha creado esto.
# Básicamente es un limite maximo de imagenes que se conservaran por cada personaje
# Eres libre de que si no te molesta tener cientos de imagenes, borrar esto.
MAX_IMAGENES_POR_CARPETA = 5  

# Diccionario de personajes y sus etiquetas exactas de busqueda en Wallhaven
# El formato es: "Nombre_Carpeta": "Terminos de busqueda"
# Puedes cambiar a tu gusto. Yo recomiendo estas Waifus
# Si tu personaje no es muy conocida, agrega más etiquetas.
PERSONAJES = {
    "Echidna": 'Echidna Re:Zero',
    "Monika": 'Monika Doki Doki Literature Club',
    "Najimi": 'Ajimu Najimi Medaka Box',
    "Samus": 'Samus Aran',
    "Ryuko": 'Ryuko Matoi Kill La Kill',
    "Frederica": 'Frederica Re:Zero',
    "Crusch": 'Crusch Karsten Re:Zero',
    "Elsa": 'Elsa Granhiert Re:Zero',
    "Mercy": 'Mercy Overwatch'
}

# Cabeceras web (Headers) para simular que la peticion viene de un navegador real (Chrome en Windows)
# Así vamos a evitar que la API de Wallhaven bloquee la conexion por detectar un script automatizado.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def limpiar_carpetas():
    # Funcion que revisa el directorio de imagenes y borra las mas antiguas
    # conservando unicamente el limite establecido en MAX_IMAGENES_POR_CARPETA
    # De esa forma, te aseguras de que no tengan cientos.
    print("\n[!] === INICIANDO LIMPIEZA DE MANTENIMIENTO ===")
    if not os.path.exists(DIRECTORIO):
        return

    # Iteramos sobre cada subcarpeta (cada personaje) dentro del directorio principal
    for personaje in os.listdir(DIRECTORIO):
        ruta_personaje = os.path.join(DIRECTORIO, personaje)
        
        if os.path.isdir(ruta_personaje):
            # Filtramos para obtener unicamente archivos que sean imagenes
            archivos = [os.path.join(ruta_personaje, f) for f in os.listdir(ruta_personaje) if f.endswith(('.jpg', '.png', '.jpeg'))]
            
            # Comparamos la cantidad de archivos con el limite permitido
            if len(archivos) > MAX_IMAGENES_POR_CARPETA:
                # Ordenamos la lista de archivos basandonos en su fecha de modificacion (los mas viejos al inicio)
                archivos.sort(key=os.path.getmtime)
                
                # Cortamos la lista para obtener solo los archivos sobrantes que deben ser eliminados
                archivos_a_borrar = archivos[:-MAX_IMAGENES_POR_CARPETA]
                
                # Ejecutamos el borrado archivo por archivo
                for archivo in archivos_a_borrar:
                    try:
                        os.remove(archivo)
                        print(f"[-] Eliminando imagen antigua de {personaje}: {os.path.basename(archivo)}")
                    except Exception as e:
                        print(f"[!] Error al borrar {archivo}: {e}")
                
                print(f"[*] Carpeta de {personaje} optimizada (Mantiene las {MAX_IMAGENES_POR_CARPETA} mas recientes).")
    print("=== MANTENIMIENTO FINALIZADO ===\n")

def obtener_wallpaper(personaje, query):
    # Funcion principal de red: consulta la API de Wallhaven y descarga la imagen
    # ratios=16x9 restringe la resolucion a monitores panoramicos
    # purity=100 asegura que solo se obtengan imagenes seguras (SFW)
    # sorting=random garantiza resultados variados en cada busqueda.
    url = f"https://wallhaven.cc/api/v1/search?q={query}&ratios=16x9&purity=100&sorting=random"
    
    try:
        print(f"[*] Buscando wallpaper de {personaje} en Wallhaven...")
        req = requests.get(url, headers=HEADERS, timeout=10)
        data = req.json()
        
        # Validamos si la respuesta de la API contiene datos en la clave 'data'
        if not data.get('data'):
            print(f"[-] No se encontraron resultados en linea. Buscando local...")
            return buscar_local(personaje)
            
        # Elegimos un resultado al azar de la lista proporcionada por Wallhaven
        img_info = random.choice(data['data'])
        img_url = img_info['path']
        nombre_archivo = os.path.basename(img_url)
        
        # Preparamos las carpetas locales para guardar la imagen
        carpeta = os.path.join(DIRECTORIO, personaje)
        os.makedirs(carpeta, exist_ok=True)
        ruta_local = os.path.join(carpeta, nombre_archivo)
        
        # Descargamos el archivo solo si no existe previamente en nuestra maquina
        if not os.path.exists(ruta_local):
            print(f"[+] Descargando nueva imagen de {personaje}...")
            # timeout=15 previene que el script se quede colgado esperando una imagen pesada
            # Siéntete libre cambiarlo
            img_data = requests.get(img_url, headers=HEADERS, timeout=15).content
            with open(ruta_local, 'wb') as f:
                f.write(img_data)
        else:
            print(f"[*] La imagen de {personaje} ya estaba descargada.")
                
        return ruta_local
        
    except Exception as e:
        # En caso de corte de internet o bloqueo de API, ejecutamos el modo offline
        print(f"[!] Error de red ({e}). Usando archivo local...")
        return buscar_local(personaje)

def buscar_local(personaje):
    # Modo de respaldo (offline). Intenta buscar una imagen local
    #Ovbiamente de Pictures.
    if not os.path.exists(DIRECTORIO): 
        print("[-] La carpeta local no existe aun.")
        return None
        
    archivos = []
    ruta_personaje = os.path.join(DIRECTORIO, personaje)
    
    # 1. Primero intenta recolectar imagenes especificas del personaje solicitado
    if os.path.exists(ruta_personaje):
        for file in os.listdir(ruta_personaje):
            if file.endswith(('.jpg', '.png', '.jpeg')):
                archivos.append(os.path.join(ruta_personaje, file))
                
    # 2. Si no hay imagenes de ese personaje, escanea el directorio entero buscando cualquier otra opcion
    if not archivos:
        print(f"[-] No hay imagenes guardadas de {personaje}, buscando otro al azar...")
        for root, dirs, files in os.walk(DIRECTORIO):
            for file in files:
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    archivos.append(os.path.join(root, file))
                
    # Si encontro archivos, devuelve uno al azar
    if archivos:
        elegido = random.choice(archivos)
        print(f"[*] Usando imagen guardada: {os.path.basename(elegido)}")
        return elegido
    else:
        # Si la carpeta total esta vacia, indica el fallo total
        print("[-] La carpeta esta vacia. No hay nada que mostrar offline.")
        return None

def main():
    # Creamos el directorio base al arrancar por si no existe
    os.makedirs(DIRECTORIO, exist_ok=True)
    print("=== Iniciando AutoWallpaper ===")
    
    # Ejecutamos la limpieza inicial
    limpiar_carpetas()
    tiempo_ultima_limpieza = time.time()
    
    # Inicializamos la lista vacia para el sistema anti-repeticion
    personajes_disponibles = []
    
    while True:
        # Verificamos si han pasado 24 horas (86400 segundos) desde el ultimo mantenimiento
        if time.time() - tiempo_ultima_limpieza >= 86400:
            limpiar_carpetas()
            tiempo_ultima_limpieza = time.time()

        # Sistema de baraja: si la lista esta vacia, la rellenamos y la mezclamos
        if not personajes_disponibles:
            personajes_disponibles = list(PERSONAJES.keys())
            random.shuffle(personajes_disponibles)
            print("\n[!] === BARAJA REINICIADA Y MEZCLADA ===")
            print(f"[*] Orden para esta ronda: {', '.join(personajes_disponibles)}\n")
            
        # Extraemos el ultimo elemento de la baraja mezclada
        personaje_actual = personajes_disponibles.pop()
        query_actual = PERSONAJES[personaje_actual]
        
        # Intentamos obtener la ruta del fondo
        wallpaper = obtener_wallpaper(personaje_actual, query_actual)
        
        # Si se obtuvo exitosamente, se envia la orden al motor grafico
        if wallpaper:
            subprocess.run(COMANDO.format(path=wallpaper), shell=True)
            print(f"[+] Fondo de {personaje_actual} aplicado exitosamente.")
        else:
            print(f"[-] No se pudo aplicar ningun fondo de {personaje_actual} esta vez.")
            
        print(f"[*] Faltan por mostrar {len(personajes_disponibles)} personajes antes de reiniciar la baraja.")
        print(f"[*] Esperando {TIEMPO_MINUTOS} minutos para el siguiente cambio...\n")
        
        # Pausamos el programa durante los minutos configurados
        time.sleep(TIEMPO_MINUTOS * 60)

if __name__ == "__main__":
    main()
# Eres libre de modificar cualquier variable!

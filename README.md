# Auto Wallpaper para Wayland (Probado en CachyOS + Hyprland + Calestia Dots, Wallhaven API)

Un script ligero y autonomo en Python disenado para entornos Wayland que cambia tu fondo de pantalla automaticamente usando la API de Wallhaven. Ideal para tus Wifus o alguna otra preferencia.

## Vistas Previas de los fondos

Aqui puedes ver algunos ejemplos de Wifus:

![Escritorio con Elsa](screenshots/Ejemplo1.jpeg)
![Escritorio con Las Dokis](screenshots/Ejemplo3.jpeg)
![Escritorio con Re:Zero](screenshots/Ejemplo5.jpeg)

Caracteristicas Principales
- **Descarga Inteligente:** Busca imagenes en resolucion 16:9 y pureza SFW directamente desde Wallhaven. Puedes cambiar esto *cof cof* ya sabes para qué cosa.
- **Sistema Anti-Repeticion:** Utiliza un sistema de "baraja" para asegurar que todos los personajes o etiquetas configuradas se muestren al menos una vez antes de repetir algun termino.
- **Modo Offline de Respaldo:** Si no hay conexion a internet o la API de Wallhaven limita las descargas temporalmente, el script reciclara automaticamente las imagenes ya guardadas.
- **Auto-Limpieza (Cuidado del Disco):** Cada 24 horas (o al iniciar la PC), el script borra las imagenes mas antiguas y conserva unicamente las 5 mas recientes por personaje para evitar llenar el almacenamiento local.
- **Transiciones Fluidas:** Configurado por defecto para usar `awww` (compatible tambien con `swww`).

## Compatibilidad
Este script esta disenado principalmente para gestores de ventanas basados en **Wayland** (probado y optimizado en CachyOS Hyprland). Utiliza `awww`/`swww` como motor de dibujo y transicion. No es compatible de forma nativa con entornos antiguos en X11 (como i3 o bspwm) ni con entornos de escritorio completos que controlan estrictamente su propio fondo (como KDE Plasma o GNOME).

## Dependencias Requeridas
Para que el script funcione correctamente, tu sistema debe contar con:
- `python`
- `python-requests`
- `awww` (o `swww`)

## Para la Instalacion y Uso

1. **Solo debes instalar dependencias:** 
   Asegurate de instalar Python y la libreria requests desde tu gestor de paquetes, preguntale a tu IA de confianza si tienes otro. Por ejemplo, en Arch Linux o CachyOS:
   ```bash
   sudo pacman -S python-request


2. **Guardar el archivo principal:**
Descarga el archivo autowallpaper.py y guardalo en tu directorio de scripts de Hyprland, por ejemplo en: ~/.config/hypr/scripts/

3. **Otorgar permisos de ejecucion:**
Abre una terminal y haz que el script sea ejecutable por el sistema:
   ```bash
   chmod +x ~/.config/hypr/scripts/autowallpaper.py

5. **Configuracion interna:**
Puedes abrir autowallpaper.py con cualquier editor de texto para modificar el diccionario PERSONAJES e incluir tus propios terminos de busqueda o ajustar la variable TIEMPO_MINUTOS segun tus preferencias.

6. **Automatizacion (Autostart):**
Para que inicie solo cada vez que enciendes la computadora, anade estas dos lineas a tu archivo de configuracion hyprland.conf:
   ```bash
   exec-once = awww-daemon &
   exec-once = python ~/.config/hypr/scripts/autowallpaper.py &

*Una advertencia: Si utilizas otro gestor de fondos por defecto como hyprpaper, asegurate de desactivarlo para evitar conflictos graficos.

A disfrutar!!

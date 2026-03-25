import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🌲 Cubicador IA de Trozas")
st.write("Sube una foto de los troncos para detectar y contar.")

# Configuración lateral
largo = st.sidebar.number_input("Largo de troza (m)", value=2.5)

img_file = st.file_uploader("Capturar o subir foto", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Procesar imagen
    image = Image.open(img_file)
    img = np.array(image)
    img_display = img.copy()
    
    # Convertir a escala de grises para la IA
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)

    # Detectar círculos (Ajustable)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 40, 
                               param1=50, param2=35, minRadius=15, maxRadius=150)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Dibujar círculos verdes en los troncos detectados
            cv2.circle(img_display, (i[0], i[1]), i[2], (0, 255, 0), 8)
        
        st.image(img_display, caption=f"Se detectaron {len(circles[0])} trozas", use_container_width=True)
        st.success(f"✅ Conteo: {len(circles[0])} trozas | Volumen Est: {(len(circles[0]) * 0.15 * largo):.2f} m³")
    else:
        st.image(img, caption="Imagen original", use_container_width=True)
        st.warning("No se detectaron círculos. Intenta una foto más clara o de frente.")

st.info("Nota: Para precisión profesional se requiere calibrar píxeles vs cm.")

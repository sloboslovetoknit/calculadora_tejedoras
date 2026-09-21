import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import os

# Función para redondear con la regla round half up
def redondear(valor):
    d = Decimal(str(valor))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

# Configuración de la página
st.set_page_config(
    page_title="Calculadora para Tejedoras",
    page_icon="🧶",
    layout="centered"
)

# --- APLICACIÓN DE ESTILOS PERSONALIZADOS ---
# Nude: #f7edec | Café: #644b3f | Fucsia: #a02c89 | Azul Claro: #e3f2fd
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f7edec;
        color: #644b3f;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;
    }
    
    /* Textos y Encabezados */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #644b3f !important;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', sans-serif;
    }

    /* Subtítulo grande y destacado */
    .subtitulo-destacado {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        color: #644b3f !important;
        margin-top: -10px;
        margin-bottom: 20px;
        line-height: 1.4;
    }
    
    /* AUMENTAR TAMAÑO DE ETIQUETAS Y CASILLAS EN MÓVIL */
    label p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }
    
    input {
        font-size: 1.25rem !important;
        padding: 10px !important;
        color: #644b3f !important;
    }
    
    /* BOTONES TODOS EN FUCSIA CON LETRA BLANCA */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #a02c89 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
        width: 100% !important;
    }
    
    /* Texto dentro del botón (forzar blanco) */
    div.stButton > button p, div.stDownloadButton > button p, div.stButton > button span {
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #80226d !important;
        color: #ffffff !important;
    }

    /* RECUADRO INICIAL DE ADVERTENCIA EN AZUL CLARO DIRECTO */
    .recuadro-azul-advertencia {
        background-color: #e3f2fd !important;
        color: #e3f2fd !important;
        border: 1px solid #b8daff !important;
        border-radius: 8px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }

    /* RECUADROS FUCSIA PARA RESULTADOS */
    .recuadro-fucsia {
        background-color: #a02c89 !important;
        color: #ffffff !important;
        padding: 16px !important;
        border-radius: 8px !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }

    /* Radio Buttons y Selectores */
    div[data-baseweb="radio"] label p {
        color: #644b3f !important;
        font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA CON LOGO Y ENLACE ---
col_logo, col_titulo = st.columns([1, 3])

logo_cargado = False
with col_logo:
    for pos_nombre in ["Logo.png.png", "logo.png", "Logo.PNG", "logo.PNG"]:
        if os.path.exists(pos_nombre):
            st.image(pos_nombre, width=130)
            logo_cargado = True
            break
    if not logo_cargado:
        st.markdown("# 🧶")

with col_titulo:
    st.title("Calculadora para Tejedoras")
    st.markdown("[👉 Visita El Club de la Madeja](https://susanacuervolobos.substack.com/)", unsafe_allow_html=True)

# --- SUBTÍTULO DESTACADO CON CORREO Y FUENTE MÁS GRANDE ---
st.markdown(
    '<p class="subtitulo-destacado">Calcula las medidas exactas para tus proyectos de tejido.<br>'
    '✉️ Consultas: <a href="mailto:info@susanalobosdesigns.com" style="color: #a02c89; text-decoration: underline;">info@susanalobosdesigns.com</a></p>', 
    unsafe_allow_html=True
)

# --- NOTA EN RECUADRO INICIAL (AZUL CLARO CON LETRAS OSCURAS) ---
st.markdown(
    '<div class="recuadro-azul-advertencia">⚠️ <i>Es importante hacer tu muestra de tensión para que las medidas se ajusten bien a tu silueta.</i></div>', 
    unsafe_allow_html=True
)

# --- IDENTIFICACIÓN DEL PROYECTO ---
st.subheader("📋 Datos del Proyecto")
col_p1, col_p2 = st.columns(2)
with col_p1:
    nombre_usuario = st.text_input("Nombre de la tejedora:", value="Alumna")
with col_p2:
    nombre_proyecto = st.text_input("Nombre del proyecto:", value="Mi Prenda")

fecha_actual = datetime.now().strftime("%Y-%m-%d")

# --- 1. DATOS DE LA MUESTRA ---
st.header("1. Datos de la Muestra de Tensión")
col1, col2 = st.columns(2)
with col1:
    pts_10cm = st.number_input("¿Cuántos puntos tienes en 10 cm?", min_value=1.0, value=20.0, step=0.5)
with col2:
    vtas_10cm = st.number_input("¿Cuántas vueltas o filas tienes en 10 cm?", min_value=1.0, value=28.0, step=0.5)

pts_por_cm = pts_10cm / 10.0
vtas_por_cm = vtas_10cm / 10.0

st.markdown(
    f'<div class="recuadro-fucsia">Tensión calculada en 1 cm: <b>{pts_por_cm:.1f} pts/cm</b> | <b>{vtas_por_cm:.1f} vtas/filas por cm</b></div>', 
    unsafe_allow_html=True
)

# --- 2. MEDIDAS DE LA PRENDA ---
st.header("2. Medidas de la Prenda")
col3, col4 = st.columns(2)
with col3:
    contorno_pecho = st.number_input("¿Qué contorno de pecho quieres? (en cm)", min_value=1.0, value=100.0, step=1.0)
with col4:
    largo_prenda = st.number_input("¿Qué largo quieres para tu prenda? (en cm)", min_value=1.0, value=60.0, step=1.0)

pts_finales = redondear(contorno_pecho * pts_por_cm)
vtas_filas_finales = redondear(largo_prenda * vtas_por_cm)

st.markdown(
    f'<div class="recuadro-fucsia"><b>Puntos necesarios:</b> {pts_finales} pts<br><br><b>Vueltas / Filas necesarias:</b> {vtas_filas_finales} vtas/filas</div>', 
    unsafe_allow_html=True
)

# --- 3. MEDIDAS LIBRES ---
st.header("3. Medidas Libres (Mangas, Puños, Escote)")
tipo_medida = st.radio("Selecciona el tipo de medida:", ["Ancho (Puntos)", "Largo (Vueltas/Filas)"])
nombre_medida = st.text_input("Nombre de la medida libre:", value="Ancho de puño")
cm_libre = st.number_input(f"¿Cuántos cm mide '{nombre_medida}'?:", min_value=0.1, value=18.0, step=0.5)

if tipo_medida == "Ancho (Puntos)":
    res_libre = redondear(cm_libre * pts_por_cm)
    texto_libre = f"Para {nombre_medida} ({cm_libre} cm) necesitas: {res_libre} pts"
else:
    res_libre = redondear(cm_libre * vtas_por_cm)
    texto_libre = f"Para {nombre_medida} ({cm_libre} cm) necesitas: {res_libre} vtas/filas"

st.write(f"=> **{texto_libre}**")

# --- BOTONES DE DESCARGA Y LIMPIEZA ---
st.write("---")
col_btn1, col_btn2 = st.columns(2)

resumen_texto = f"""========================================
RESUMEN DE MI PROYECTO - EL CLUB DE LA MADEJA
========================================
Fecha: {fecha_actual}
Tejedora: {nombre_usuario}
Proyecto: {nombre_proyecto}

MUESTRA DE TENSIÓN:
- Puntos en 10 cm: {pts_10cm} ({pts_por_cm:.1f} pts/cm)
- Vueltas/Filas en 10 cm: {vtas_10cm} ({vtas_por_cm:.1f} vtas/filas por cm)

CÁLCULOS DE LA PRENDA:
- Contorno ({contorno_pecho} cm): {pts_finales} puntos
- Largo ({largo_prenda} cm): {vtas_filas_finales} vueltas/filas

MEDIDA LIBRE:
- {texto_libre}

========================================
     © 2026 Susana Lobos García
Contacto: info@susanalobosdesigns.com
.:. Visita el Club de la Madeja .:.
https://susanacuervolobos.substack.com/
========================================
"""

with col_btn1:
    st.download_button(
        label="📥 Descargar resumen (.txt)",
        data=resumen_texto,
        file_name=f"Resumen_Tejido_{nombre_proyecto.replace(' ', '_')}.txt",
        mime="text/plain"
    )

with col_btn2:
    if st.button("🔄 Reiniciar / Limpiar datos"):
        st.rerun()

# --- COPYRIGHT Y CONTACTO AL FINAL ---
st.write("---")
st.caption("© 2026 Susana Lobos García - Club de la Madeja. Todos los derechos reservados.")
st.caption("📧 Consultas y preguntas: info@susanalobosdesigns.com")

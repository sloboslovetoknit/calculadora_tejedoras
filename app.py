import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import os

# Función para redondear con la regla round half up
def redondear(valor):
    d = Decimal(str(valor))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

# Muestra un número con hasta 2 decimales, sin ceros sobrantes (2.25 / 2.5 / 2)
def fmt(valor):
    d = Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f"{d:.2f}".rstrip("0").rstrip(".")

# Muestra un valor con su unidad, o una raya si la casilla está vacía (para el resumen)
def valor_o_raya(valor, unidad=""):
    return f"{fmt(valor)}{unidad}" if valor is not None else "—"

# Configuración de la página
st.set_page_config(
    page_title="Calculadora para Tejedoras",
    page_icon="🧶",
    layout="centered"
)

# --- ESTADO DE LA APP ---
# Casillas que se vacían al apretar "Reiniciar / Limpiar datos"
CAMPOS_GENERALES = [
    "nombre_usuario", "nombre_proyecto",
    "pts_10cm", "vtas_10cm",
    "contorno_cuerpo", "holgura", "largo_prenda",
]
PREFIJOS_MEDIDA = ("nombre_medida_", "tipo_medida_", "cm_libre_")

# Lista de medidas libres (cada una con un número de identificación propio)
if "medidas" not in st.session_state:
    st.session_state.medidas = [0]
    st.session_state.siguiente_id = 1

def borrar_casillas_de_medida(id_medida):
    for prefijo in PREFIJOS_MEDIDA:
        st.session_state.pop(f"{prefijo}{id_medida}", None)

def agregar_medida():
    st.session_state.medidas.append(st.session_state.siguiente_id)
    st.session_state.siguiente_id += 1

def quitar_medida(id_medida):
    st.session_state.medidas.remove(id_medida)
    borrar_casillas_de_medida(id_medida)

# Botón de limpiar: deja todas las casillas en blanco y una sola medida libre
def limpiar_datos():
    for campo in CAMPOS_GENERALES:
        st.session_state.pop(campo, None)
    for id_medida in st.session_state.medidas:
        borrar_casillas_de_medida(id_medida)
    st.session_state.medidas = [st.session_state.siguiente_id]
    st.session_state.siguiente_id += 1

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
        color:  #644b3f !important;
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

    /* RECUADRO DE ESPERA (cuando aún faltan datos para calcular) */
    .recuadro-pendiente {
        background-color: transparent !important;
        color: #644b3f !important;
        border: 1px dashed #644b3f !important;
        border-radius: 8px !important;
        padding: 14px !important;
        font-size: 1.05rem !important;
        font-style: italic;
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

def recuadro_fucsia(html):
    st.markdown(f'<div class="recuadro-fucsia">{html}</div>', unsafe_allow_html=True)

def recuadro_pendiente(texto):
    st.markdown(f'<div class="recuadro-pendiente">{texto}</div>', unsafe_allow_html=True)

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
    nombre_usuario = st.text_input("Nombre de la tejedora:", placeholder="Ej: Alumna", key="nombre_usuario")
with col_p2:
    nombre_proyecto = st.text_input("Nombre del proyecto:", placeholder="Ej: Mi Prenda", key="nombre_proyecto")

fecha_actual = datetime.now().strftime("%Y-%m-%d")

# --- 1. DATOS DE LA MUESTRA ---
st.header("1. Datos de la Muestra de Tensión")
col1, col2 = st.columns(2)
with col1:
    pts_10cm = st.number_input("¿Cuántos puntos tienes en 10 cm?", min_value=1.0, value=None,
                               step=0.5, placeholder="Ej: 20", key="pts_10cm")
with col2:
    vtas_10cm = st.number_input("¿Cuántas vueltas o filas tienes en 10 cm?", min_value=1.0, value=None,
                                step=0.5, placeholder="Ej: 28", key="vtas_10cm")

pts_por_cm = pts_10cm / 10.0 if pts_10cm is not None else None
vtas_por_cm = vtas_10cm / 10.0 if vtas_10cm is not None else None

if pts_por_cm is None and vtas_por_cm is None:
    recuadro_pendiente("Escribe los puntos y vueltas de tu muestra para ver tu tensión en 1 cm.")
else:
    partes = []
    if pts_por_cm is not None:
        partes.append(f"<b>{fmt(pts_por_cm)} pts/cm</b>")
    if vtas_por_cm is not None:
        partes.append(f"<b>{fmt(vtas_por_cm)} vtas/filas por cm</b>")
    recuadro_fucsia("Tensión calculada en 1 cm: " + " | ".join(partes))

# --- 2. MEDIDAS DE LA PRENDA ---
st.header("2. Medidas de la Prenda")
col3, col4 = st.columns(2)
with col3:
    contorno_cuerpo = st.number_input("Contorno de pecho de tu cuerpo (en cm)", min_value=1.0, value=None,
                                      step=1.0, placeholder="Ej: 90", key="contorno_cuerpo")
with col4:
    holgura = st.number_input(
        "Holgura que quieres agregar (en cm)", min_value=-50.0, value=None, step=1.0,
        placeholder="Ej: 10", key="holgura",
        help="La holgura es la diferencia entre tu cuerpo y la prenda. Puede ser 0, positiva "
             "(prenda más suelta) o negativa (prenda más ajustada). Si la dejas vacía, se cuenta como 0."
    )
largo_prenda = st.number_input("¿Qué largo quieres para tu prenda? (en cm)", min_value=1.0, value=None,
                               step=1.0, placeholder="Ej: 60", key="largo_prenda")

holgura_cm = holgura if holgura is not None else 0.0
contorno_prenda = contorno_cuerpo + holgura_cm if contorno_cuerpo is not None else None
pts_finales = None
vtas_filas_finales = None

lineas = []
if contorno_prenda is not None and contorno_prenda <= 0:
    recuadro_pendiente("La holgura negativa es mayor que el contorno del cuerpo. Revisa los números.")
    contorno_prenda = None
elif contorno_prenda is not None:
    texto = f"<b>Contorno de la prenda:</b> {fmt(contorno_prenda)} cm"
    if holgura_cm != 0:
        signo = "+" if holgura_cm > 0 else "−"
        texto += f" ({fmt(contorno_cuerpo)} cm {signo} {fmt(abs(holgura_cm))} cm de holgura)"
    lineas.append(texto)
    if pts_por_cm is not None:
        pts_finales = redondear(contorno_prenda * pts_por_cm)
        lineas.append(f"<b>Puntos necesarios:</b> {pts_finales} pts")
if largo_prenda is not None and vtas_por_cm is not None:
    vtas_filas_finales = redondear(largo_prenda * vtas_por_cm)
    lineas.append(f"<b>Vueltas / Filas necesarias:</b> {vtas_filas_finales} vtas/filas")

if lineas:
    recuadro_fucsia("<br><br>".join(lineas))
else:
    recuadro_pendiente("Completa tu muestra y las medidas para ver cuántos puntos y vueltas necesitas.")

# --- 3. MEDIDAS LIBRES ---
st.header("3. Medidas Libres (Mangas, Puños, Escote)")
st.markdown("Agrega todas las medidas que necesites para tu proyecto.")

resumen_medidas = []
for numero, id_medida in enumerate(list(st.session_state.medidas), start=1):
    with st.container(border=True):
        st.markdown(f"**Medida {numero}**")
        nombre_medida = st.text_input("Nombre de la medida:", placeholder="Ej: Ancho de puño",
                                      key=f"nombre_medida_{id_medida}")
        tipo_medida = st.radio("Tipo de medida:", ["Ancho (Puntos)", "Largo (Vueltas/Filas)"],
                               horizontal=True, key=f"tipo_medida_{id_medida}")
        etiqueta = nombre_medida.strip() or "esta medida"
        cm_libre = st.number_input(f"¿Cuántos cm mide {etiqueta}?", min_value=0.1, value=None,
                                   step=0.5, placeholder="Ej: 18", key=f"cm_libre_{id_medida}")

        es_ancho = tipo_medida == "Ancho (Puntos)"
        por_cm = pts_por_cm if es_ancho else vtas_por_cm
        unidad = "pts" if es_ancho else "vtas/filas"

        if cm_libre is None:
            recuadro_pendiente("Escribe los cm para ver el resultado.")
        elif por_cm is None:
            recuadro_pendiente("Completa tu muestra de tensión (sección 1) para ver el resultado.")
        else:
            res_libre = redondear(cm_libre * por_cm)
            recuadro_fucsia(f"Para <b>{etiqueta}</b> ({fmt(cm_libre)} cm) necesitas: <b>{res_libre} {unidad}</b>")
            resumen_medidas.append(f"- {etiqueta} ({fmt(cm_libre)} cm): {res_libre} {unidad}")

        if len(st.session_state.medidas) > 1:
            st.button("🗑️ Quitar esta medida", key=f"quitar_{id_medida}",
                      on_click=quitar_medida, args=(id_medida,))

st.button("➕ Agregar otra medida", on_click=agregar_medida)

# --- BOTONES DE DESCARGA Y LIMPIEZA ---
st.write("---")
col_btn1, col_btn2 = st.columns(2)

texto_medidas = "\n".join(resumen_medidas) if resumen_medidas else "- (sin medidas libres)"
pts_por_cm_txt = f" ({fmt(pts_por_cm)} pts/cm)" if pts_por_cm is not None else ""
vtas_por_cm_txt = f" ({fmt(vtas_por_cm)} vtas/filas por cm)" if vtas_por_cm is not None else ""

resumen_texto = f"""========================================
RESUMEN DE MI PROYECTO - EL CLUB DE LA MADEJA
========================================
Fecha: {fecha_actual}
Tejedora: {nombre_usuario or "—"}
Proyecto: {nombre_proyecto or "—"}

MUESTRA DE TENSIÓN:
- Puntos en 10 cm: {valor_o_raya(pts_10cm)}{pts_por_cm_txt}
- Vueltas/Filas en 10 cm: {valor_o_raya(vtas_10cm)}{vtas_por_cm_txt}

CÁLCULOS DE LA PRENDA:
- Contorno del cuerpo: {valor_o_raya(contorno_cuerpo, " cm")}
- Holgura: {fmt(holgura_cm)} cm
- Contorno de la prenda ({valor_o_raya(contorno_prenda, " cm")}): {pts_finales if pts_finales is not None else "—"} puntos
- Largo ({valor_o_raya(largo_prenda, " cm")}): {vtas_filas_finales if vtas_filas_finales is not None else "—"} vueltas/filas

MEDIDAS LIBRES:
{texto_medidas}

========================================
     © 2026 Susana Lobos García
Contacto: info@susanalobosdesigns.com
.:. Visita el Club de la Madeja .:.
https://susanacuervolobos.substack.com/
========================================
"""

nombre_archivo = (nombre_proyecto.strip() or "Mi_Prenda").replace(" ", "_")

with col_btn1:
    st.download_button(
        label="📥 Descargar resumen (.txt)",
        data=resumen_texto,
        file_name=f"Resumen_Tejido_{nombre_archivo}.txt",
        mime="text/plain"
    )

with col_btn2:
    st.button("🔄 Reiniciar / Limpiar datos", on_click=limpiar_datos)

# --- COPYRIGHT Y CONTACTO AL FINAL ---
st.write("---")
st.caption("© 2026 Susana Lobos García - Club de la Madeja. Todos los derechos reservados.")
st.caption("📧 Consultas y preguntas: info@susanalobosdesigns.com")

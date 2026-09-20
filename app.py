import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

def redondear(valor):
    d = Decimal(str(valor))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

st.set_page_config(page_title="Calculadora para Tejedoras", page_icon="🧶")

st.title("Calculadora de Puntos y Vueltas para Prendas Tejidas 🧶")

st.write("Calcula las medidas exactas para tus proyectos de tejido.")
# --- NOTA EN RECUADRO CON LETRA CURSIVA ---
st.warning("*Es importante hacer tu muestra de tensión para que las medidas se ajusten bien a tu silueta.*")

# --- 1. DATOS DE LA MUESTRA ---
st.header("1. Datos de la Muestra de Tensión")
col1, col2 = st.columns(2)
with col1:
    pts_10cm = st.number_input("¿Cuántos puntos tienes en 10 cm?", min_value=1.0, value=20.0, step=0.5)
with col2:
    vtas_10cm = st.number_input("¿Cuántas vueltas o filas tienes en 10 cm?", min_value=1.0, value=28.0, step=0.5)

pts_por_cm = pts_10cm / 10.0
vtas_por_cm = vtas_10cm / 10.0

st.info(f"Tensión calculada en 1 cm: **{pts_por_cm:.1f} pts/cm** | **{vtas_por_cm:.1f} vtas/cm**")

# --- 2. MEDIDAS DE LA PRENDA ---
st.header("2. Medidas de la Prenda")
col3, col4 = st.columns(2)
with col3:
    contorno_pecho = st.number_input("¿Qué contorno quieres? (en cm)", min_value=1.0, value=100.0, step=1.0)
with col4:
    largo_prenda = st.number_input("¿Qué largo quieres? (en cm)", min_value=1.0, value=60.0, step=1.0)

pts_finales = redondear(contorno * pts_por_cm)
vtas_finales = redondear(largo * vtas_por_cm)

st.success(f"**Puntos necesarios:** {pts_finales} pts\n\n**Vueltas o Filas necesarias:** {vtas_filas_finales} vtas")

# --- 3. MEDIDAS LIBRES ---
st.header("3. Medidas Libres (Mangas, Puños, Escote)")
tipo_medida = st.radio("Selecciona el tipo de medida:", ["Ancho (Puntos)", "Largo (Vueltas)"])
nombre_medida = st.text_input("Nombre de la medida (ej. Ancho de puño):", value="Ancho de puño")
cm_libre = st.number_input(f"¿Cuántos cm mide '{nombre_medida}'?:", min_value=0.1, value=18.0, step=0.5)

if tipo_medida == "Ancho (Puntos)":
    res_libre = redondear(cm_libre * pts_por_cm)
    st.write(f"=> Para **{nombre_medida}** ({cm_libre} cm) necesitas: **{res_libre} pts**")
else:
    res_libre = redondear(cm_libre * vtas_por_cm)
    st.write(f"=> Para **{nombre_medida}** ({cm_libre} cm) necesitas: **{res_libre} vtas**")
    
    # --- COPYRIGHT AL FINAL ---
st.write("--")
st.write("--")
st.caption("© 2026 Susana Lobos García - Club de la Madeja. Todos los derechos reservados.")

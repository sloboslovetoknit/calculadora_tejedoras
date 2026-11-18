import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import os

# Round using the "round half up" rule
def round_half_up(value):
    d = Decimal(str(value))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

# Show a number with up to 2 decimals, without extra zeros (2.25 / 2.5 / 2)
def fmt(value):
    d = Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f"{d:.2f}".rstrip("0").rstrip(".")

# Show a value with its unit, or a dash if the field is empty (for the summary)
def value_or_dash(value, unit=""):
    return f"{fmt(value)}{unit}" if value is not None else "—"

# Page setup
st.set_page_config(
    page_title="Knitting Calculator",
    page_icon="🧶",
    layout="centered"
)

# --- APP STATE ---
# Fields that are cleared by the "Reset / Clear data" button
GENERAL_FIELDS = [
    "knitter_name", "project_name",
    "sts_10cm", "rows_10cm",
    "body_chest", "ease", "garment_length",
]
MEASUREMENT_PREFIXES = ("measurement_name_", "measurement_type_", "measurement_cm_")

# List of custom measurements (each one with its own ID number)
if "measurements" not in st.session_state:
    st.session_state.measurements = [0]
    st.session_state.next_id = 1

def clear_measurement_fields(measurement_id):
    for prefix in MEASUREMENT_PREFIXES:
        st.session_state.pop(f"{prefix}{measurement_id}", None)

def add_measurement():
    st.session_state.measurements.append(st.session_state.next_id)
    st.session_state.next_id += 1

def remove_measurement(measurement_id):
    st.session_state.measurements.remove(measurement_id)
    clear_measurement_fields(measurement_id)

# Reset button: empties every field and leaves a single custom measurement
def clear_data():
    for field in GENERAL_FIELDS:
        st.session_state.pop(field, None)
    for measurement_id in st.session_state.measurements:
        clear_measurement_fields(measurement_id)
    st.session_state.measurements = [st.session_state.next_id]
    st.session_state.next_id += 1

# --- CUSTOM STYLES ---
# Nude: #f7edec | Brown: #644b3f | Fuchsia: #a02c89 | Light blue: #e3f2fd
st.markdown("""
    <style>
    /* General background */
    .stApp {
        background-color: #f7edec;
        color: #644b3f;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;
    }

    /* Text and headings */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #644b3f !important;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', sans-serif;
    }

    /* Large, highlighted subtitle */
    .subtitulo-destacado {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        color: #644b3f !important;
        margin-top: -10px;
        margin-bottom: 20px;
        line-height: 1.4;
    }

    /* LARGER LABELS AND FIELDS ON MOBILE */
    label p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }

    input {
        font-size: 1.25rem !important;
        padding: 10px !important;
        color: #644b3f !important;
    }

    /* ALL BUTTONS IN FUCHSIA WITH WHITE TEXT */
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

    /* Text inside buttons (force white) */
    div.stButton > button p, div.stDownloadButton > button p, div.stButton > button span {
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #80226d !important;
        color: #ffffff !important;
    }

    /* INITIAL NOTE IN LIGHT BLUE */
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

    /* FUCHSIA BOXES FOR RESULTS */
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

    /* WAITING BOX (when data is still missing) */
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

    /* Radio buttons and selectors */
    div[data-baseweb="radio"] label p {
        color: #644b3f !important;
        font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def result_box(html):
    st.markdown(f'<div class="recuadro-fucsia">{html}</div>', unsafe_allow_html=True)

def waiting_box(text):
    st.markdown(f'<div class="recuadro-pendiente">{text}</div>', unsafe_allow_html=True)

# --- HEADER WITH LOGO AND LINK ---
col_logo, col_title = st.columns([1, 3])

logo_loaded = False
with col_logo:
    for file_name in ["Logo.png.png", "logo.png", "Logo.PNG", "logo.PNG"]:
        if os.path.exists(file_name):
            st.image(file_name, width=130)
            logo_loaded = True
            break
    if not logo_loaded:
        st.markdown("# 🧶")

with col_title:
    st.title("Knitting Calculator")
    st.markdown("[👉 Visit One Skein Club](https://oneskeinclub.substack.com/)", unsafe_allow_html=True)

# --- HIGHLIGHTED SUBTITLE WITH EMAIL ---
st.markdown(
    '<p class="subtitulo-destacado">Calculate the exact numbers for your knitting projects.<br>'
    '✉️ Questions: <a href="mailto:info@susanalobosdesigns.com" style="color: #a02c89; text-decoration: underline;">info@susanalobosdesigns.com</a></p>',
    unsafe_allow_html=True
)

# --- INITIAL NOTE (LIGHT BLUE BOX) ---
st.markdown(
    '<div class="recuadro-azul-advertencia">⚠️ <i>Knitting a gauge swatch is important so your measurements fit your body well.</i></div>',
    unsafe_allow_html=True
)

# --- PROJECT DETAILS ---
st.subheader("📋 Project Details")
col_p1, col_p2 = st.columns(2)
with col_p1:
    knitter_name = st.text_input("Knitter's name:", placeholder="e.g. Student", key="knitter_name")
with col_p2:
    project_name = st.text_input("Project name:", placeholder="e.g. My Sweater", key="project_name")

current_date = datetime.now().strftime("%Y-%m-%d")

# --- 1. GAUGE SWATCH ---
st.header("1. Gauge Swatch")
col1, col2 = st.columns(2)
with col1:
    sts_10cm = st.number_input("How many stitches do you have in 10 cm?", min_value=1.0, value=None,
                               step=0.5, placeholder="e.g. 20", key="sts_10cm")
with col2:
    rows_10cm = st.number_input("How many rows or rounds do you have in 10 cm?", min_value=1.0, value=None,
                                step=0.5, placeholder="e.g. 28", key="rows_10cm")

sts_per_cm = sts_10cm / 10.0 if sts_10cm is not None else None
rows_per_cm = rows_10cm / 10.0 if rows_10cm is not None else None

if sts_per_cm is None and rows_per_cm is None:
    waiting_box("Enter the stitches and rows from your swatch to see your gauge per 1 cm.")
else:
    parts = []
    if sts_per_cm is not None:
        parts.append(f"<b>{fmt(sts_per_cm)} sts/cm</b>")
    if rows_per_cm is not None:
        parts.append(f"<b>{fmt(rows_per_cm)} rows/rnds per cm</b>")
    result_box("Gauge per 1 cm: " + " | ".join(parts))

# --- 2. GARMENT MEASUREMENTS ---
st.header("2. Garment Measurements")
col3, col4 = st.columns(2)
with col3:
    body_chest = st.number_input("Your body's chest circumference (in cm)", min_value=1.0, value=None,
                                 step=1.0, placeholder="e.g. 90", key="body_chest")
with col4:
    ease = st.number_input(
        "Ease you want to add (in cm)", min_value=-50.0, value=None, step=1.0,
        placeholder="e.g. 10", key="ease",
        help="Ease is the difference between your body and the garment. It can be zero, positive "
             "(a looser fit) or negative (a closer fit). If you leave it empty, it counts as 0."
    )
garment_length = st.number_input("How long do you want your garment to be? (in cm)", min_value=1.0, value=None,
                                 step=1.0, placeholder="e.g. 60", key="garment_length")

ease_cm = ease if ease is not None else 0.0
garment_chest = body_chest + ease_cm if body_chest is not None else None
total_sts = None
total_rows = None

lines = []
if garment_chest is not None and garment_chest <= 0:
    waiting_box("The negative ease is larger than your body's circumference. Please check the numbers.")
    garment_chest = None
elif garment_chest is not None:
    text = f"<b>Garment circumference:</b> {fmt(garment_chest)} cm"
    if ease_cm != 0:
        sign = "+" if ease_cm > 0 else "−"
        text += f" ({fmt(body_chest)} cm {sign} {fmt(abs(ease_cm))} cm of ease)"
    lines.append(text)
    if sts_per_cm is not None:
        total_sts = round_half_up(garment_chest * sts_per_cm)
        lines.append(f"<b>Stitches needed:</b> {total_sts} sts")
if garment_length is not None and rows_per_cm is not None:
    total_rows = round_half_up(garment_length * rows_per_cm)
    lines.append(f"<b>Rows / Rounds needed:</b> {total_rows} rows/rnds")

if lines:
    result_box("<br><br>".join(lines))
else:
    waiting_box("Complete your swatch and measurements to see how many stitches and rows you need.")

# --- 3. CUSTOM MEASUREMENTS ---
st.header("3. Custom Measurements (Sleeves, Cuffs, Neckline)")
st.markdown("Add as many measurements as you need for your project.")

summary_measurements = []
for number, measurement_id in enumerate(list(st.session_state.measurements), start=1):
    with st.container(border=True):
        st.markdown(f"**Measurement {number}**")
        measurement_name = st.text_input("Measurement name:", placeholder="e.g. Cuff width",
                                         key=f"measurement_name_{measurement_id}")
        measurement_type = st.radio("Type of measurement:", ["Width (Stitches)", "Length (Rows/Rounds)"],
                                    horizontal=True, key=f"measurement_type_{measurement_id}")
        label = measurement_name.strip() or "this measurement"
        measurement_cm = st.number_input(f"How many cm is {label}?", min_value=0.1, value=None,
                                         step=0.5, placeholder="e.g. 18", key=f"measurement_cm_{measurement_id}")

        is_width = measurement_type == "Width (Stitches)"
        per_cm = sts_per_cm if is_width else rows_per_cm
        unit = "sts" if is_width else "rows/rnds"

        if measurement_cm is None:
            waiting_box("Enter the cm to see the result.")
        elif per_cm is None:
            waiting_box("Complete your gauge swatch (section 1) to see the result.")
        else:
            result = round_half_up(measurement_cm * per_cm)
            result_box(f"For <b>{label}</b> ({fmt(measurement_cm)} cm) you need: <b>{result} {unit}</b>")
            summary_measurements.append(f"- {label} ({fmt(measurement_cm)} cm): {result} {unit}")

        if len(st.session_state.measurements) > 1:
            st.button("🗑️ Remove this measurement", key=f"remove_{measurement_id}",
                      on_click=remove_measurement, args=(measurement_id,))

st.button("➕ Add another measurement", on_click=add_measurement)

# --- DOWNLOAD AND RESET BUTTONS ---
st.write("---")
col_btn1, col_btn2 = st.columns(2)

measurements_text = "\n".join(summary_measurements) if summary_measurements else "- (no custom measurements)"
sts_per_cm_txt = f" ({fmt(sts_per_cm)} sts/cm)" if sts_per_cm is not None else ""
rows_per_cm_txt = f" ({fmt(rows_per_cm)} rows/rnds per cm)" if rows_per_cm is not None else ""

summary_text = f"""========================================
MY PROJECT SUMMARY - ONE SKEIN CLUB
========================================
Date: {current_date}
Knitter: {knitter_name or "—"}
Project: {project_name or "—"}

GAUGE SWATCH:
- Stitches in 10 cm: {value_or_dash(sts_10cm)}{sts_per_cm_txt}
- Rows/Rounds in 10 cm: {value_or_dash(rows_10cm)}{rows_per_cm_txt}

GARMENT CALCULATIONS:
- Body chest circumference: {value_or_dash(body_chest, " cm")}
- Ease: {fmt(ease_cm)} cm
- Garment circumference ({value_or_dash(garment_chest, " cm")}): {total_sts if total_sts is not None else "—"} stitches
- Length ({value_or_dash(garment_length, " cm")}): {total_rows if total_rows is not None else "—"} rows/rounds

CUSTOM MEASUREMENTS:
{measurements_text}

========================================
     © 2026 Susana Lobos García
Contact: info@susanalobosdesigns.com
.:. Visit One Skein Club .:.
https://oneskeinclub.substack.com/
========================================
"""

file_label = (project_name.strip() or "My_Project").replace(" ", "_")

with col_btn1:
    st.download_button(
        label="📥 Download summary (.txt)",
        data=summary_text,
        file_name=f"Knitting_Summary_{file_label}.txt",
        mime="text/plain"
    )

with col_btn2:
    st.button("🔄 Reset / Clear data", on_click=clear_data)

# --- COPYRIGHT AND CONTACT ---
st.write("---")
st.caption("© 2026 Susana Lobos García - One Skein Club. All rights reserved.")
st.caption("📧 Questions and inquiries: info@susanalobosdesigns.com")

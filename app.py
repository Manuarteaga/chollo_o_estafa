import datetime
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CholloScore | Analizador Inteligente de Coches de Ocasión",
    page_icon="🚗",
    layout="wide",
)

# Identidad visual oscura (Slate / Navy + esmeralda/cielo) alineada con PrimaScore
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        .stApp {
            background-color: #090d16;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            background-image:
                radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 50%);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        code, pre, [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.78);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(51, 65, 85, 0.65);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        }
        div[data-testid="stMetric"] {
            background: rgba(9, 13, 22, 0.72);
            border: 1px solid rgba(51, 65, 85, 0.75);
            border-radius: 14px;
            padding: 14px 16px;
        }
        div[data-testid="stMetricLabel"] > div {
            color: #94a3b8;
            font-size: 0.78rem;
        }
        div[data-testid="stMetricValue"] > div {
            color: #f8fafc;
            font-weight: 700;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #0d9488 100%);
            color: #090d16;
            font-weight: 700;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1.2rem;
        }
        .stButton > button[kind="primary"]:hover {
            filter: brightness(1.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabecera superior estilo PrimaScore
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(15,23,42,0.85);border:1px solid rgba(51,65,85,0.75);border-radius:14px;padding:14px 20px;margin-bottom:18px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#10b981,#0d9488);display:flex;align-items:center;justify-content:center;color:#090d16;font-weight:800;">
                🚗
            </div>
            <div>
                <div style="font-size:1.1rem;font-weight:700;color:#ffffff;">
                    Chollo<span style="color:#34d399;">Score</span>
                    <span style="margin-left:8px;font-size:0.68rem;font-family:'JetBrains Mono',monospace;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:#1e293b;color:#94a3b8;border:1px solid #334155;">Coches de Ocasión</span>
                </div>
                <div style="font-size:0.8rem;color:#94a3b8;">Auditoría de precio al contado, depreciación y financiación</div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:999px;background:rgba(16,185,129,0.12);color:#34d399;border:1px solid rgba(16,185,129,0.25);font-size:0.75rem;font-family:'JetBrains Mono',monospace;">
            <span style="width:7px;height:7px;border-radius:50%;background:#34d399;display:inline-block;"></span>
            Auditor Activo
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Base de datos ampliada (incluye marcas chinas como BYD y Omoda + modelos actuales)
BASE_DATOS_COCHES = {
    "Audi": {
        "A1": {"precio_nuevo": 24500, "potencia": 110, "combustible": "Gasolina", "transmisión": "Manual"},
        "A3": {"precio_nuevo": 31000, "potencia": 116, "combustible": "Gasolina", "transmisión": "Manual"},
        "A4": {"precio_nuevo": 42000, "potencia": 163, "combustible": "Diésel", "transmisión": "Automática"},
        "A5": {"precio_nuevo": 52000, "potencia": 204, "combustible": "Híbrido", "transmisión": "Automática"},
        "A6": {"precio_nuevo": 57000, "potencia": 204, "combustible": "Diésel", "transmisión": "Automática"},
        "Q2": {"precio_nuevo": 29500, "potencia": 116, "combustible": "Gasolina", "transmisión": "Manual"},
        "Q3": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Q5": {"precio_nuevo": 53000, "potencia": 204, "combustible": "Diésel", "transmisión": "Automática"},
    },
    "BMW": {
        "Serie 1": {"precio_nuevo": 32000, "potencia": 136, "combustible": "Gasolina", "transmisión": "Automática"},
        "Serie 2": {"precio_nuevo": 36500, "potencia": 156, "combustible": "Gasolina", "transmisión": "Automática"},
        "Serie 3": {"precio_nuevo": 43000, "potencia": 184, "combustible": "Diésel", "transmisión": "Automática"},
        "Serie 5": {"precio_nuevo": 58000, "potencia": 190, "combustible": "Diésel", "transmisión": "Automática"},
        "X1": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
        "X3": {"precio_nuevo": 54000, "potencia": 190, "combustible": "Híbrido", "transmisión": "Automática"},
        "X5": {"precio_nuevo": 78000, "potencia": 286, "combustible": "Híbrido", "transmisión": "Automática"},
        "iX1": {"precio_nuevo": 48500, "potencia": 204, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
    },
    "BYD": {
        "Dolphin": {"precio_nuevo": 30500, "potencia": 177, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Dolphin Surf": {"precio_nuevo": 19990, "potencia": 88, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Atto 2": {"precio_nuevo": 29990, "potencia": 177, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Atto 3": {"precio_nuevo": 37990, "potencia": 204, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Seal": {"precio_nuevo": 46990, "potencia": 313, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Seal U": {"precio_nuevo": 42290, "potencia": 218, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Seal U DM-i": {"precio_nuevo": 38990, "potencia": 218, "combustible": "Híbrido Enchufe (PHEV)", "transmisión": "Automática"},
    },
    "Cupra": {
        "Formentor": {"precio_nuevo": 34500, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Leon": {"precio_nuevo": 29500, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Ateca": {"precio_nuevo": 33000, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Born": {"precio_nuevo": 37500, "potencia": 204, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Terramar": {"precio_nuevo": 41500, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Dacia": {
        "Sandero": {"precio_nuevo": 14500, "potencia": 100, "combustible": "GLP / GNC", "transmisión": "Manual"},
        "Duster": {"precio_nuevo": 20500, "potencia": 130, "combustible": "Híbrido", "transmisión": "Manual"},
        "Jogger": {"precio_nuevo": 19500, "potencia": 110, "combustible": "GLP / GNC", "transmisión": "Manual"},
        "Bigster": {"precio_nuevo": 25500, "potencia": 155, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Ford": {
        "Fiesta": {"precio_nuevo": 18000, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Focus": {"precio_nuevo": 26000, "potencia": 125, "combustible": "Gasolina", "transmisión": "Manual"},
        "Puma": {"precio_nuevo": 24500, "potencia": 125, "combustible": "Híbrido", "transmisión": "Manual"},
        "Kuga": {"precio_nuevo": 33000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Honda": {
        "Civic": {"precio_nuevo": 32000, "potencia": 184, "combustible": "Híbrido", "transmisión": "Automática"},
        "HR-V": {"precio_nuevo": 33000, "potencia": 131, "combustible": "Híbrido", "transmisión": "Automática"},
        "CR-V": {"precio_nuevo": 43000, "potencia": 184, "combustible": "Híbrido", "transmisión": "Automática"},
        "Jazz": {"precio_nuevo": 24500, "potencia": 109, "combustible": "Híbrido", "transmisión": "Automática"},
        "ZR-V": {"precio_nuevo": 38500, "potencia": 184, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Hyundai": {
        "i20": {"precio_nuevo": 18000, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "i30": {"precio_nuevo": 23500, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Kona": {"precio_nuevo": 26500, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Tucson": {"precio_nuevo": 32500, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Santa Fe": {"precio_nuevo": 47000, "potencia": 215, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Kia": {
        "Picanto": {"precio_nuevo": 14500, "potencia": 67, "combustible": "Gasolina", "transmisión": "Manual"},
        "Ceed": {"precio_nuevo": 22500, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Stonic": {"precio_nuevo": 21000, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "XCeed": {"precio_nuevo": 25500, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Sportage": {"precio_nuevo": 32000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Sorento": {"precio_nuevo": 45000, "potencia": 215, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Mercedes-Benz": {
        "Clase A": {"precio_nuevo": 34000, "potencia": 136, "combustible": "Gasolina", "transmisión": "Automática"},
        "Clase C": {"precio_nuevo": 48000, "potencia": 200, "combustible": "Híbrido", "transmisión": "Automática"},
        "Clase E": {"precio_nuevo": 61000, "potencia": 197, "combustible": "Diésel", "transmisión": "Automática"},
        "GLA": {"precio_nuevo": 41000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
        "GLC": {"precio_nuevo": 60000, "potencia": 197, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "MG": {
        "MG3 Hybrid+": {"precio_nuevo": 19990, "potencia": 194, "combustible": "Híbrido", "transmisión": "Automática"},
        "ZS": {"precio_nuevo": 17500, "potencia": 106, "combustible": "Gasolina", "transmisión": "Manual"},
        "ZS Hybrid+": {"precio_nuevo": 23490, "potencia": 197, "combustible": "Híbrido", "transmisión": "Automática"},
        "HS": {"precio_nuevo": 29990, "potencia": 170, "combustible": "Gasolina", "transmisión": "Automática"},
        "MG4": {"precio_nuevo": 30690, "potencia": 170, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
    },
    "Omoda": {
        "Omoda 5": {"precio_nuevo": 27290, "potencia": 185, "combustible": "Gasolina", "transmisión": "Automática"},
        "Omoda 5 EV": {"precio_nuevo": 37900, "potencia": 204, "combustible": "Eléctrico (EV)", "transmisión": "Automática"},
        "Omoda 7": {"precio_nuevo": 34500, "potencia": 195, "combustible": "Híbrido", "transmisión": "Automática"},
        "Omoda 9": {"precio_nuevo": 44900, "potencia": 450, "combustible": "Híbrido Enchufe (PHEV)", "transmisión": "Automática"},
    },
    "Peugeot": {
        "208": {"precio_nuevo": 19000, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "2008": {"precio_nuevo": 24500, "potencia": 130, "combustible": "Gasolina", "transmisión": "Automática"},
        "308": {"precio_nuevo": 26500, "potencia": 130, "combustible": "Gasolina", "transmisión": "Manual"},
        "3008": {"precio_nuevo": 35500, "potencia": 136, "combustible": "Híbrido", "transmisión": "Automática"},
        "5008": {"precio_nuevo": 39500, "potencia": 136, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Renault": {
        "Clio": {"precio_nuevo": 18500, "potencia": 90, "combustible": "Gasolina", "transmisión": "Manual"},
        "Captur": {"precio_nuevo": 23500, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "Megane": {"precio_nuevo": 27000, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "Austral": {"precio_nuevo": 32500, "potencia": 200, "combustible": "Híbrido", "transmisión": "Automática"},
        "Arkana": {"precio_nuevo": 29500, "potencia": 145, "combustible": "Híbrido", "transmisión": "Automática"},
        "Symbioz": {"precio_nuevo": 30500, "potencia": 145, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Seat": {
        "Ibiza": {"precio_nuevo": 19500, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Leon": {"precio_nuevo": 25000, "potencia": 115, "combustible": "Gasolina", "transmisión": "Manual"},
        "Arona": {"precio_nuevo": 22500, "potencia": 110, "combustible": "Gasolina", "transmisión": "Manual"},
        "Ateca": {"precio_nuevo": 28500, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Tarraco": {"precio_nuevo": 35500, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
    },
    "Toyota": {
        "Yaris": {"precio_nuevo": 21500, "potencia": 116, "combustible": "Híbrido", "transmisión": "Automática"},
        "Yaris Cross": {"precio_nuevo": 26500, "potencia": 116, "combustible": "Híbrido", "transmisión": "Automática"},
        "Corolla": {"precio_nuevo": 26500, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "C-HR": {"precio_nuevo": 31500, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "RAV4": {"precio_nuevo": 40500, "potencia": 218, "combustible": "Híbrido", "transmisión": "Automática"},
        "Camry": {"precio_nuevo": 43000, "potencia": 218, "combustible": "Híbrido", "transmisión": "Automática"},
    },
    "Volkswagen": {
        "Polo": {"precio_nuevo": 21500, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Golf": {"precio_nuevo": 31500, "potencia": 130, "combustible": "Gasolina", "transmisión": "Manual"},
        "T-Roc": {"precio_nuevo": 28500, "potencia": 115, "combustible": "Gasolina", "transmisión": "Manual"},
        "Tiguan": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Passat": {"precio_nuevo": 42000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
    },
}

ENTIDADES_FINANCIERAS = [
    {"entidad": "ING (Préstamo Naranja Coches)", "tin": 5.49, "destacado": "Sin comisiones y 100% online"},
    {"entidad": "BBVA (Préstamo Coche Online)", "tin": 5.95, "destacado": "Respuesta rápida para clientes y no clientes"},
    {"entidad": "Openbank (Préstamo Personal)", "tin": 4.95, "destacado": "El interés más bajo si domicilias nómina"},
    {"entidad": "Banco Santander (Préstamo Coche)", "tin": 6.25, "destacado": "Financiación flexible hasta 8 años"},
    {"entidad": "Younited Credit", "tin": 5.75, "destacado": "Plataforma 100% digital rápida"},
]


def resolver_marca_en_bd(texto_marca: str):
    """Devuelve la clave exacta de BASE_DATOS_COCHES si coincide de forma exacta o parcial."""
    limpio = (texto_marca or "").strip().lower()
    if not limpio or limpio.startswith("--"):
        return None
    for clave in BASE_DATOS_COCHES:
        if clave.lower() == limpio:
            return clave
    for clave in BASE_DATOS_COCHES:
        if clave.lower().startswith(limpio) or (len(limpio) >= 3 and limpio in clave.lower()):
            return clave
    return None


def formato_es(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_cuota_francesa(capital, tin, meses):
    if tin == 0 or meses == 0:
        return capital / max(1, meses)
    r = (tin / 100) / 12
    return capital * (r * ((1 + r) ** meses)) / (((1 + r) ** meses) - 1)


st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### 📋 Datos del Vehículo y Financiación")

col_m1, col_m2 = st.columns(2)

with col_m1:
    opciones_marcas = ["-- Selecciona o escribe abajo --"] + sorted(list(BASE_DATOS_COCHES.keys()))
    marca_sel = st.selectbox("Marca del Vehículo", options=opciones_marcas)
    marca_man = st.text_input(
        "¿Otra marca o búsqueda directa? Escríbela aquí (ej. BYD, Omoda, Cupra...):",
        value="",
    ).strip()

    marca_coincidente = resolver_marca_en_bd(marca_man) if marca_man else resolver_marca_en_bd(marca_sel)
    if marca_man:
        marca_final = marca_coincidente if marca_coincidente else marca_man.title()
    else:
        marca_final = marca_coincidente if marca_coincidente else "Marca no especificada"

    # Al escribir una marca (en la caja de texto o seleccionándola), cargamos sus modelos automáticamente
    modelos_disponibles = list(BASE_DATOS_COCHES.get(marca_coincidente or marca_final, {}).keys())
    opciones_modelos = (
        ["-- Selecciona un modelo o escríbelo abajo --"] + modelos_disponibles
        if modelos_disponibles
        else ["-- Escribe el modelo abajo --"]
    )
    default_modelo_idx = 1 if modelos_disponibles else 0

    modelo_sel = st.selectbox(
        "Modelo del Vehículo (se actualiza según la marca escrita)",
        options=opciones_modelos,
        index=default_modelo_idx,
    )
    modelo_man = st.text_input("¿Otro modelo? Escríbelo aquí:", value="").strip()

    if modelo_man:
        modelo_final = modelo_man
    elif not modelo_sel.startswith("--"):
        modelo_final = modelo_sel
    else:
        modelo_final = "Modelo no especificado"

    precio_sugerido = 25000.0
    potencia_sugerida =

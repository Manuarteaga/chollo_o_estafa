import json
import os
import streamlit as st

st.set_page_config(
    page_title="Chollo o Estafa | Auditor de Precios y Financiación de Coches",
    page_icon="🚗",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #090d16;
            color: #f8fafc;
        }
        .block-container {
            padding-top: 0.75rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DATOS_COCHES = {
    "Audi": {
        "A1": {"precio_nuevo": 24500, "potencia": 110, "combustible": "Gasolina", "transmision": "Manual"},
        "A3": {"precio_nuevo": 31000, "potencia": 116, "combustible": "Gasolina", "transmision": "Manual"},
        "A4": {"precio_nuevo": 42000, "potencia": 163, "combustible": "Diésel", "transmision": "Automática"},
        "A5": {"precio_nuevo": 52000, "potencia": 204, "combustible": "Híbrido", "transmision": "Automática"},
        "A6": {"precio_nuevo": 57000, "potencia": 204, "combustible": "Diésel", "transmision": "Automática"},
        "Q2": {"precio_nuevo": 29500, "potencia": 116, "combustible": "Gasolina", "transmision": "Manual"},
        "Q3": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Gasolina", "transmision": "Automática"},
        "Q5": {"precio_nuevo": 53000, "potencia": 204, "combustible": "Diésel", "transmision": "Automática"},
    },
    "BMW": {
        "Serie 1": {"precio_nuevo": 32000, "potencia": 136, "combustible": "Gasolina", "transmision": "Automática"},
        "Serie 2": {"precio_nuevo": 36500, "potencia": 156, "combustible": "Gasolina", "transmision": "Automática"},
        "Serie 3": {"precio_nuevo": 43000, "potencia": 184, "combustible": "Diésel", "transmision": "Automática"},
        "Serie 5": {"precio_nuevo": 58000, "potencia": 190, "combustible": "Diésel", "transmision": "Automática"},
        "X1": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Diésel", "transmision": "Automática"},
        "X3": {"precio_nuevo": 54000, "potencia": 190, "combustible": "Híbrido", "transmision": "Automática"},
        "X5": {"precio_nuevo": 78000, "potencia": 286, "combustible": "Híbrido", "transmision": "Automática"},
        "iX1": {"precio_nuevo": 48500, "potencia": 204, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
    },
    "BYD": {
        "Dolphin": {"precio_nuevo": 30500, "potencia": 177, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Dolphin Surf": {"precio_nuevo": 19990, "potencia": 88, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Atto 2": {"precio_nuevo": 29990, "potencia": 177, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Atto 3": {"precio_nuevo": 37990, "potencia": 204, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Seal": {"precio_nuevo": 46990, "potencia": 313, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Seal U": {"precio_nuevo": 42290, "potencia": 218, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Seal U DM-i": {"precio_nuevo": 38990, "potencia": 218, "combustible": "Híbrido Enchufe (PHEV)", "transmision": "Automática"},
    },
    "Cupra": {
        "Formentor": {"precio_nuevo": 34500, "potencia": 150, "combustible": "Gasolina", "transmision": "Automática"},
        "Leon": {"precio_nuevo": 29500, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
        "Ateca": {"precio_nuevo": 33000, "potencia": 150, "combustible": "Gasolina", "transmision": "Automática"},
        "Born": {"precio_nuevo": 37500, "potencia": 204, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Terramar": {"precio_nuevo": 41500, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Dacia": {
        "Sandero": {"precio_nuevo": 14500, "potencia": 100, "combustible": "GLP / GNC", "transmision": "Manual"},
        "Duster": {"precio_nuevo": 20500, "potencia": 130, "combustible": "Híbrido", "transmision": "Manual"},
        "Jogger": {"precio_nuevo": 19500, "potencia": 110, "combustible": "GLP / GNC", "transmision": "Manual"},
        "Bigster": {"precio_nuevo": 25500, "potencia": 155, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Ford": {
        "Fiesta": {"precio_nuevo": 18000, "potencia": 95, "combustible": "Gasolina", "transmision": "Manual"},
        "Focus": {"precio_nuevo": 26000, "potencia": 125, "combustible": "Gasolina", "transmision": "Manual"},
        "Puma": {"precio_nuevo": 24500, "potencia": 125, "combustible": "Híbrido", "transmision": "Manual"},
        "Kuga": {"precio_nuevo": 33000, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Honda": {
        "Civic": {"precio_nuevo": 32000, "potencia": 184, "combustible": "Híbrido", "transmision": "Automática"},
        "HR-V": {"precio_nuevo": 33000, "potencia": 131, "combustible": "Híbrido", "transmision": "Automática"},
        "CR-V": {"precio_nuevo": 43000, "potencia": 184, "combustible": "Híbrido", "transmision": "Automática"},
        "Jazz": {"precio_nuevo": 24500, "potencia": 109, "combustible": "Híbrido", "transmision": "Automática"},
        "ZR-V": {"precio_nuevo": 38500, "potencia": 184, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Hyundai": {
        "i20": {"precio_nuevo": 18000, "potencia": 100, "combustible": "Gasolina", "transmision": "Manual"},
        "i30": {"precio_nuevo": 23500, "potencia": 120, "combustible": "Gasolina", "transmision": "Manual"},
        "Kona": {"precio_nuevo": 26500, "potencia": 120, "combustible": "Gasolina", "transmision": "Manual"},
        "Tucson": {"precio_nuevo": 32500, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
        "Santa Fe": {"precio_nuevo": 47000, "potencia": 215, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Kia": {
        "Picanto": {"precio_nuevo": 14500, "potencia": 67, "combustible": "Gasolina", "transmision": "Manual"},
        "Ceed": {"precio_nuevo": 22500, "potencia": 120, "combustible": "Gasolina", "transmision": "Manual"},
        "Stonic": {"precio_nuevo": 21000, "potencia": 100, "combustible": "Gasolina", "transmision": "Manual"},
        "XCeed": {"precio_nuevo": 25500, "potencia": 120, "combustible": "Gasolina", "transmision": "Manual"},
        "Sportage": {"precio_nuevo": 32000, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
        "Sorento": {"precio_nuevo": 45000, "potencia": 215, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Mercedes-Benz": {
        "Clase A": {"precio_nuevo": 34000, "potencia": 136, "combustible": "Gasolina", "transmision": "Automática"},
        "Clase C": {"precio_nuevo": 48000, "potencia": 200, "combustible": "Híbrido", "transmision": "Automática"},
        "Clase E": {"precio_nuevo": 61000, "potencia": 197, "combustible": "Diésel", "transmision": "Automática"},
        "GLA": {"precio_nuevo": 41000, "potencia": 150, "combustible": "Diésel", "transmision": "Automática"},
        "GLC": {"precio_nuevo": 60000, "potencia": 197, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "MG": {
        "MG3 Hybrid+": {"precio_nuevo": 19990, "potencia": 194, "combustible": "Híbrido", "transmision": "Automática"},
        "ZS": {"precio_nuevo": 17500, "potencia": 106, "combustible": "Gasolina", "transmision": "Manual"},
        "ZS Hybrid+": {"precio_nuevo": 23490, "potencia": 197, "combustible": "Híbrido", "transmision": "Automática"},
        "HS": {"precio_nuevo": 29990, "potencia": 170, "combustible": "Gasolina", "transmision": "Automática"},
        "MG4": {"precio_nuevo": 30690, "potencia": 170, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
    },
    "Omoda": {
        "Omoda 5": {"precio_nuevo": 27290, "potencia": 185, "combustible": "Gasolina", "transmision": "Automática"},
        "Omoda 5 EV": {"precio_nuevo": 37900, "potencia": 204, "combustible": "Eléctrico (EV)", "transmision": "Automática"},
        "Omoda 7": {"precio_nuevo": 34500, "potencia": 195, "combustible": "Híbrido", "transmision": "Automática"},
        "Omoda 9": {"precio_nuevo": 44900, "potencia": 450, "combustible": "Híbrido Enchufe (PHEV)", "transmision": "Automática"},
    },
    "Peugeot": {
        "208": {"precio_nuevo": 19000, "potencia": 100, "combustible": "Gasolina", "transmision": "Manual"},
        "2008": {"precio_nuevo": 24500, "potencia": 130, "combustible": "Gasolina", "transmision": "Automática"},
        "308": {"precio_nuevo": 26500, "potencia": 130, "combustible": "Gasolina", "transmision": "Manual"},
        "3008": {"precio_nuevo": 35500, "potencia": 136, "combustible": "Híbrido", "transmision": "Automática"},
        "5008": {"precio_nuevo": 39500, "potencia": 136, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Renault": {
        "Clio": {"precio_nuevo": 18500, "potencia": 90, "combustible": "Gasolina", "transmision": "Manual"},
        "Captur": {"precio_nuevo": 23500, "potencia": 100, "combustible": "Gasolina", "transmision": "Manual"},
        "Megane": {"precio_nuevo": 27000, "potencia": 140, "combustible": "Híbrido", "transmision": "Automática"},
        "Austral": {"precio_nuevo": 32500, "potencia": 200, "combustible": "Híbrido", "transmision": "Automática"},
        "Arkana": {"precio_nuevo": 29500, "potencia": 145, "combustible": "Híbrido", "transmision": "Automática"},
        "Symbioz": {"precio_nuevo": 30500, "potencia": 145, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Seat": {
        "Ibiza": {"precio_nuevo": 19500, "potencia": 95, "combustible": "Gasolina", "transmision": "Manual"},
        "Leon": {"precio_nuevo": 25000, "potencia": 115, "combustible": "Gasolina", "transmision": "Manual"},
        "Arona": {"precio_nuevo": 22500, "potencia": 110, "combustible": "Gasolina", "transmision": "Manual"},
        "Ateca": {"precio_nuevo": 28500, "potencia": 150, "combustible": "Gasolina", "transmision": "Automática"},
        "Tarraco": {"precio_nuevo": 35500, "potencia": 150, "combustible": "Diésel", "transmision": "Automática"},
    },
    "Toyota": {
        "Yaris": {"precio_nuevo": 21500, "potencia": 116, "combustible": "Híbrido", "transmision": "Automática"},
        "Yaris Cross": {"precio_nuevo": 26500, "potencia": 116, "combustible": "Híbrido", "transmision": "Automática"},
        "Corolla": {"precio_nuevo": 26500, "potencia": 140, "combustible": "Híbrido", "transmision": "Automática"},
        "C-HR": {"precio_nuevo": 31500, "potencia": 140, "combustible": "Híbrido", "transmision": "Automática"},
        "RAV4": {"precio_nuevo": 40500, "potencia": 218, "combustible": "Híbrido", "transmision": "Automática"},
        "Camry": {"precio_nuevo": 43000, "potencia": 218, "combustible": "Híbrido", "transmision": "Automática"},
    },
    "Volkswagen": {
        "Polo": {"precio_nuevo": 21500, "potencia": 95, "combustible": "Gasolina", "transmision": "Manual"},
        "Golf": {"precio_nuevo": 31500, "potencia": 130, "combustible": "Gasolina", "transmision": "Manual"},
        "T-Roc": {"precio_nuevo": 28500, "potencia": 115, "combustible": "Gasolina", "transmision": "Manual"},
        "Tiguan": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
        "Passat": {"precio_nuevo": 42000, "potencia": 150, "combustible": "Híbrido", "transmision": "Automática"},
    },
}

ENTIDADES_FINANCIERAS = [
    {"entidad": "ING (Préstamo Naranja Coches)", "tin": 5.49, "destacado": "Sin comisiones y 100% online"},
    {"entidad": "BBVA (Préstamo Coche Online)", "tin": 5.95, "destacado": "Respuesta rápida para clientes y no clientes"},
    {"entidad": "Openbank (Préstamo Personal)", "tin": 4.95, "destacado": "El interés más bajo si domicilias nómina"},
    {"entidad": "Banco Santander (Préstamo Coche)", "tin": 6.25, "destacado": "Financiación flexible hasta 8 años"},
    {"entidad": "Younited Credit", "tin": 5.75, "destacado": "Plataforma 100% digital rápida"},
]

html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    datos_json = json.dumps(BASE_DATOS_COCHES, ensure_ascii=False)
    bancos_json = json.dumps(ENTIDADES_FINANCIERAS, ensure_ascii=False)

    inyector = f"""
    <script>
        window.BASE_DATOS_COCHES = {datos_json};
        window.ENTIDADES_FINANCIERAS = {bancos_json};
        if (typeof inicializarAppCoches === "function") {{
            inicializarAppCoches();
        }}
    </script>
    </body>
    """

    html_final = html_code.replace("</body>", inyector)
    st.components.v1.html(html_final, height=1380, scrolling=True)
else:
    st.error(
        "No se encuentra el archivo 'index.html'. Asegúrate de subirlo a GitHub junto con 'app.py'."
    )

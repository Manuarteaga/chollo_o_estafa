import streamlit as st
import datetime

st.title("🚗 Analizador Inteligente de Precios de Coches de Ocasión")

# Base de datos simplificada de marcas y sus modelos más comunes
BASE_MARCAS_MODELOS = {
    "Toyota": ["Yaris", "Corolla", "C-HR", "RAV4", "Camry"],
    "Honda": ["Civic", "HR-V", "CR-V", "Jazz"],
    "Volkswagen": ["Polo", "Golf", "T-Roc", "Tiguan", "Passat"],
    "Seat": ["Ibiza", "Leon", "Arona", "Ateca", "Tarraco"],
    "Renault": ["Clio", "Captur", "Megane", "Austral", "Arkana"],
    "Peugeot": ["208", "2008", "308", "3008", "5008"],
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga"],
    "Hyundai": ["i20", "i30", "Kona", "Tucson", "Santa Fe"],
    "Kia": ["Picanto", "Ceed", "Stonic", "Sportage", "Sorento"],
    "BMW": ["Serie 1", "Serie 3", "Serie 5", "X1", "X3", "X5"],
    "Mercedes-Benz": ["Clase A", "Clase C", "Clase E", "GLA", "GLC"],
    "Audi": ["A3", "A4", "A6", "Q3", "Q5"]
}

st.markdown("### 📋 Datos del Vehículo")

col_m1, col_m2 = st.columns(2)

with col_m1:
    # --- SELECCIÓN DE MARCA ---
    opciones_marcas = ["-- Selecciona o escribe abajo --"] + sorted(list(BASE_MARCAS_MODELOS.keys()))
    marca_sel = st.selectbox("Marca del Vehículo", options=opciones_marcas)
    marca_man = st.text_input("¿Otra marca? Escríbela aquí:", value="").strip()
    
    if marca_man:
        marca_final = marca_man.strip().title()
    elif not marca_sel.startswith("--"):
        marca_final = marca_sel
    else:
        marca_final = "Marca no especificada"

    # --- SELECCIÓN DE MODELO ---
    # Si la marca elegida está en nuestra base de datos, mostramos sus modelos
    modelos_disponibles = BASE_MARCAS_MODELOS.get(marca_final, [])
    opciones_modelos = ["-- Selecciona o escribe abajo --"] + modelos_disponibles
    
    modelo_sel = st.selectbox("Modelo del Vehículo", options=opciones_modelos, disabled=(marca_final == "Marca no especificada" and not marca_man))
    modelo_man = st.text_input("¿Otro modelo? Escríbelo aquí:", value="").strip()
    
    if modelo_man:
        modelo_final = modelo_man.strip().title()
    elif not modelo_sel.startswith("--"):
        modelo_final = modelo_sel
    else:
        modelo_final = "Modelo no especificado"

    precio_nuevo = st.number_input("Precio de Venta Nuevo Original (€)", min_value=0.0, value=25000.0, step=1000.0)

with col_m2:
    ano_matriculacion = st.number_input("Año de Matriculación", min_value=198

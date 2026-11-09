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
    ano_matriculacion = st.number_input("Año de Matriculación", min_value=1980, max_value=datetime.datetime.now().year, value=2020, step=1)
    km_actuales = st.number_input("Kilometraje Actual (km)", min_value=0, value=75000, step=5000)
    precio_anunciado = st.number_input("Precio al que lo estás viendo (€)", min_value=0.0, value=14500.0, step=500.0)
    etiqueta_dgt = st.selectbox("Etiqueta Ambiental DGT", ["ECO / Cero", "C", "B", "Sin Etiqueta"])

st.markdown("---")

if st.button("Analizar si está Barato, Correcto o Caro", type="primary", use_container_width=True):
    # 1. Cálculo de edad exacta
    ano_actual = datetime.datetime.now().year
    edad_anos = max(1, ano_actual - ano_matriculacion)
    
    # 2. Curva de depreciación base (15% 1er año, 8% siguientes)
    valor_teorico = precio_nuevo * ((1 - 0.15) * ((1 - 0.08) ** (edad_anos - 1)))
    
    # 3. Ajuste por kilometraje (referencia estándar: 15.000 km/año)
    km_teoricos_esperados = edad_anos * 15000
    diferencia_km = km_actuales - km_teoricos_esperados
    
    # Penalización o bonificación del 1% por cada 10.000 km de desviación
    ajuste_km_valor = (diferencia_km / 10000) * 0.01 * valor_teorico
    valor_mercado_ajustado = max(1000.0, valor_teorico - ajuste_km_valor)
    
    # 4. Cálculo de variación porcentual respecto al precio ofertado
    variacion_pct = ((precio_anunciado - valor_mercado_ajustado) / valor_mercado_ajustado) * 100
    
    # 5. Veredicto del Semáforo
    if variacion_pct <= -8.0:
        estado = "🟢 ¡MUY BARATO / OPORTUNIDAD!"
        detalle = f"El vehículo se encuentra un {abs(variacion_pct):.1f}% por debajo de su valor teórico de mercado."
    elif -8.0 < variacion_pct <= 6.0:
        estado = "🟡 PRECIO CORRECTO / JUSTO"
        detalle = "El precio anunciado se ajusta bien a su antigüedad, uso e historial de depreciación."
    else:
        estado = "🔴 CARO / SOBREVALORADO"
        detalle = f"El precio anunciado supera en un {variacion_pct:.1f}% la estimación teórica."

    # Informe final en pantalla
    st.markdown(f"### 📊 Resultado del Análisis: **{marca_final} {modelo_final}**")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Valor Teórico Estimado", f"{valor_mercado_ajustado:,.2f} €")
    m2.metric("Precio Anunciado", f"{precio_anunciado:,.2f} €")
    m3.metric("Desviación de Mercado", f"{variacion_pct:+.1f}%")
    
    st.markdown(f"#### Veredicto: {estado}")
    st.info(f"**Justificación:** {detalle}")

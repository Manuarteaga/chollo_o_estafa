import streamlit as st
import datetime

st.title("🚗 Analizador Inteligente de Precios de Coches de Ocasión")

# Lista de marcas de referencia (puedes ampliarla o ajustarla)
MARCAS_HABITUALES = [
    "-- Selecciona o escribe abajo --",
    "Audi", "BMW", "Citroën", "Cupra", "Dacia", "Fiat", "Ford", "Honda", 
    "Hyundai", "Kia", "Mazda", "Mercedes-Benz", "Nissan", "Opel", "Peugeot", 
    "Renault", "Seat", "Skoda", "Toyota", "Volkswagen", "Volvo"
]

st.markdown("### 📋 Datos del Vehículo")

col_m1, col_m2 = st.columns(2)

with col_m1:
    # 1. Selección de marca (Desplegable + Campo manual)
    marca_seleccionada = st.selectbox("Marca del Vehículo", options=MARCAS_HABITUALES)
    marca_manual = st.text_input("¿Otra marca? Escríbela aquí:", value="").strip()
    
    # Determinar la marca final introducida
    if marca_manual:
        marca_final = marca_manual.upper()
    elif not marca_seleccionada.startswith("--"):
        marca_final = marca_seleccionada
    else:
        marca_final = "No especificada"

    precio_nuevo = st.number_input("Precio de Venta Nuevo Original (€)", min_value=0.0, value=25000.0, step=1000.0)
    ano_matriculacion = st.number_input("Año de Matriculación", min_value=1980, max_value=datetime.datetime.now().year, value=2020, step=1)

with col_m2:
    precio_anunciado = st.number_input("Precio al que lo estás viendo (€)", min_value=0.0, value=14500.0, step=500.0)
    km_actuales = st.number_input("Kilometraje Actual (km)", min_value=0, value=75000, step=5000)
    etiqueta_dgt = st.selectbox("Etiqueta Ambiental DGT", ["ECO / Cero", "C", "B", "Sin Etiqueta"])

st.markdown("---")

if st.button("Analizar si está Barato, Correcto o Caro", type="primary", use_container_width=True):
    # 1. Cálculo de edad exacta
    ano_actual = datetime.datetime.now().year
    edad_anos = max(1, ano_actual - ano_matriculacion)
    
    # 2. Curva de depreciación base (15% el primer año, 8% anual los siguientes)
    valor_teorico = precio_nuevo * ((1 - 0.15) * ((1 - 0.08) ** (edad_anos - 1)))
    
    # 3. Ajuste por kilometraje (referencia: 15.000 km/año)
    km_teoricos_esperados = edad_anos * 15000
    diferencia_km = km_actuales - km_teoricos_esperados
    
    # Penalización o bonificación del 1% del valor teórico por cada 10.000 km de desviación
    ajuste_km_valor = (diferencia_km / 10000) * 0.01 * valor_teorico
    valor_mercado_ajustado = max(1000.0, valor_teorico - ajuste_km_valor)
    
    # 4. Cálculo de variación porcentual respecto al precio anunciado
    variacion_pct = ((precio_anunciado - valor_mercado_ajustado) / valor_mercado_ajustado) * 100
    
    # 5. Veredicto del Semáforo
    if variacion_pct <= -8.0:
        estado = "🟢 ¡MUY BARATO / OPORTUNIDAD!"
        detalle = f"El vehículo se encuentra un {abs(variacion_pct):.1f}% por debajo de su valor teórico de mercado."
    elif -8.0 < variacion_pct <= 6.0:
        estado = "🟡 PRECIO CORRECTO / JUSTO"
        detalle = "El precio anunciado es acorde a su antigüedad, kilometraje y depreciación."
    else:
        estado = "🔴 CARO / SOBREVALORADO"
        detalle = f"El precio anunciado supera en un {variacion_pct:.1f}% la estimación teórica de mercado."

    # Mostrar informe de resultados
    st.markdown(f"### 📊 Resultado del Análisis para: **{marca_final}**")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Valor Teórico Estimado", f"{valor_mercado_ajustado:,.2f} €")
    m2.metric("Precio Anunciado", f"{precio_anunciado:,.2f} €")
    m3.metric("Desviación de Mercado", f"{variacion_pct:+.1f}%")
    
    st.markdown(f"#### Veredicto: {estado}")
    st.info(f"**Justificación:** {detalle}")

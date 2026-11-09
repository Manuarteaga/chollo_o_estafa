import streamlit as st
import datetime

st.title("🚗 Analizador Inteligente de Precios de Coches de Ocasión")

# Entradas del usuario
col1, col2 = st.columns(2)
with col1:
    precio_nuevo = st.number_input("Precio de Venta Nuevo Original (€)", value=25000.0, step=1000.0)
    ano_matriculacion = st.number_input("Año de Matriculación", value=2020, step=1)
    km_actuales = st.number_input("Kilometraje Actual (km)", value=75000, step=5000)
with col2:
    precio_anunciado = st.number_input("Precio al que lo estás viendo (€)", value=14500.0, step=500.0)
    etiqueta_dgt = st.selectbox("Etiqueta Ambiental", ["ECO / Cero", "C", "B", "Sin Etiqueta"])

if st.button("Analizar si está Barato, Correcto o Caro", type="primary"):
    # 1. Calcular edad
    ano_actual = datetime.datetime.now().year
    edad_anos = max(1, ano_actual - ano_matriculacion)
    
    # 2. Curva de depreciación estimada (ej. 15% el 1º año, 8% los siguientes)
    valor_teorico = precio_nuevo * ((1 - 0.15) * ((1 - 0.08) ** (edad_anos - 1)))
    
    # 3. Ajuste por km (Media estándar: 15.000 km/año)
    km_teoricos_esperados = edad_anos * 15000
    diferencia_km = km_actuales - km_teoricos_esperados
    
    # Penalización o bonificación del 1% por cada 10.000 km de desviación
    ajuste_km_valor = (diferencia_km / 10000) * 0.01 * valor_teorico
    valor_mercado_ajustado = max(1000.0, valor_teorico - ajuste_km_valor)
    
    # 4. Margen de diferencia porcentual
    variacion_pct = ((precio_anunciado - valor_mercado_ajustado) / valor_mercado_ajustado) * 100
    
    # 5. Veredicto del Semáforo
    if variacion_pct <= -8.0:
        estado = "🟢 ¡MUY BARATO / OPORTUNIDAD!"
        detalle = f"El coche está un {abs(variacion_pct):.1f}% por debajo de su valor teórico de mercado."
    elif -8.0 < variacion_pct <= 6.0:
        estado = "🟡 PRECIO CORRECTO / JUSTO"
        detalle = "El precio se alinea de forma muy razonable con su edad, desgaste y depreciación."
    else:
        estado = "🔴 CARO / SOBREVALORADO"
        detalle = f"El precio supera en un {variacion_pct:.1f}% lo que correspondería por sus características."

    # Mostrar resultados con métricas visuales
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Valor Teórico Estimado", f"{valor_mercado_ajustado:,.2f} €")
    m2.metric("Precio Anunciado", f"{precio_anunciado:,.2f} €")
    m3.metric("Desviación de Mercado", f"{variacion_pct:+.1f}%")
    
    st.markdown(f"### Veredicto: {estado}")
    st.info(detalle)

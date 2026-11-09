import streamlit as st
import datetime

st.set_page_config(page_title="Analizador Inteligente de Coches de Ocasión", layout="wide")

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

st.markdown("### 📋 Datos del Vehículo y Financiación")

col_m1, col_m2 = st.columns(2)

with col_m1:
    # --- SELECCIÓN DE MARCA ---
    opciones_marcas = ["-- Selecciona o escribe abajo --"] + sorted(list(BASE_MARCAS_MODELOS.keys()))
    marca_sel = st.selectbox("Marca del Vehículo", options=opciones_marcas)
    marca_man = st.text_input("¿Otra marca? Escríbela aquí:", value="").strip()
    
    marca_final = marca_man.strip().title() if marca_man else (marca_sel if not marca_sel.startswith("--") else "Marca no especificada")

    # --- SELECCIÓN DE MODELO ---
    modelos_disponibles = list(BASE_MARCAS_MODELOS.get(marca_final, {}).keys())
    opciones_modelos = ["-- Selecciona o escribe abajo --"] + modelos_disponibles
    
    modelo_sel = st.selectbox("Modelo del Vehículo", options=opciones_modelos)
    modelo_man = st.text_input("¿Otro modelo? Escríbela aquí:", value="").strip()
    
    modelo_final = modelo_man.strip().title() if modelo_man else (modelo_sel if not modelo_sel.startswith("--") else "Modelo no especificado")

    # Autocompletar precio nuevo y especificaciones si existe en la base de datos
    precio_sugerido = 25000.0
    potencia_sugerida = 110
    combustible_sugerido = "Gasolina"
    transmision_sugerida = "Manual"

    if marca_final in BASE_DATOS_COCHES and modelo_final in BASE_MARCAS_MODELOS[marca_final]:
        datos_auto = BASE_DATOS_COCHES[marca_final][modelo_final]
        precio_sugerido = float(datos_auto["precio_nuevo"])
        potencia_sugerida = int(datos_auto["potencia"])
        combustible_sugerido = datos_auto["combustible"]
        transmision_sugerida = datos_auto["transmisión"]

    precio_nuevo = st.number_input("Precio de Venta Nuevo Original (€)", min_value=0.0, value=precio_sugerido, step=500.0, format="%.2f")
    
    # Nuevos campos técnicos solicitados
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        potencia_cv = st.number_input("Potencia (CV)", min_value=30, max_value=1000, value=potencia_sugerida, step=5)
    with col_t2:
        transmision = st.selectbox("Transmisión", ["Manual", "Automática"], index=0 if transmision_sugerida=="Manual" else 1)
        
    combustible = st.selectbox("Tipo de Combustión", ["Gasolina", "Diésel", "Híbrido", "Híbrido Enchufe (PHEV)", "Eléctrico (EV)", "GLP / GNC"], index=["Gasolina", "Diésel", "Híbrido", "Híbrido Enchufe (PHEV)", "Eléctrico (EV)", "GLP / GNC"].index(combustible_sugerido) if combustible_sugerido in ["Gasolina", "Diésel", "Híbrido", "Híbrido Enchufe (PHEV)", "Eléctrico (EV)", "GLP / GNC"] else 0)

with col_m2:
    ano_matriculacion = st.number_input("Año de Matriculación", min_value=1980, max_value=datetime.datetime.now().year, value=2020, step=1)
    km_actuales = st.number_input("Kilometraje Actual (km)", min_value=0, value=75000, step=5000)
    
    precio_contado = st.number_input("Precio al Contado (€)", min_value=0.0, value=14500.0, step=500.0, format="%.2f")
    
    # Opción de precio financiado
    tiene_financiacion = st.checkbox("¿Tiene opción o precio financiado?")
    precio_financiado = 0.0
    if tiene_financiacion:
        precio_financiado = st.number_input("Precio Total Financiado (Suma de cuotas + entrada) (€)", min_value=0.0, value=16800.0, step=500.0, format="%.2f")

    etiqueta_dgt = st.selectbox("Etiqueta Ambiental DGT", ["ECO / Cero", "C", "B", "Sin Etiqueta"])

st.markdown("---")

def formato_es(valor):
    """Convierte un número a formato español: puntos para miles y coma para decimales"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if st.button("Analizar si está Barato, Correcto o Caro", type="primary", use_container_width=True):
    # 1. Cálculo de edad exacta
    ano_actual = datetime.datetime.now().year
    edad_anos = max(1, ano_actual - ano_matriculacion)
    
    # 2. Curva de depreciación base (15% 1er año, 8% siguientes) + pequeño factor corrector por tipo de combustible
    corrector_combustible = 1.0
    if combustible in ["Híbrido", "Eléctrico (EV)", "Híbrido Enchufe (PHEV)"]:
        corrector_combustible = 1.03  # Los ECO/Cero retienen un pelín mejor su valor
        
    valor_teorico = precio_nuevo * ((1 - 0.15) * ((1 - 0.08) ** (edad_anos - 1))) * corrector_combustible
    
    # 3. Ajuste por kilometraje (referencia estándar: 15.000 km/año)
    km_teoricos_esperados = edad_anos * 15000
    diferencia_km = km_actuales - km_teoricos_esperados
    
    ajuste_km_valor = (diferencia_km / 10000) * 0.01 * valor_teorico
    valor_mercado_ajustado = max(1000.0, valor_teorico - ajuste_km_valor)
    
    # 4. Cálculo de variación porcentual respecto al precio al contado
    variacion_pct = ((precio_contado - valor_mercado_ajustado) / valor_mercado_ajustado) * 100
    
    # 5. Veredicto del Semáforo
    if variacion_pct <= -8.0:
        estado = "🟢 ¡MUY BARATO / OPORTUNIDAD!"
        detalle = f"El vehículo se encuentra un {abs(variacion_pct):.1f}% por debajo de su valor teórico de mercado al contado."
    elif -8.0 < variacion_pct <= 6.0:
        estado = "🟡 PRECIO CORRECTO / JUSTO"
        detalle = "El precio al contado anunciado se ajusta de forma equilibrada a su antigüedad, potencia, combustible y kilometraje."
    else:
        estado = "🔴 CARO / SOBREVALORADO"
        detalle = f"El precio al contado supera en un {variacion_pct:.1f}% la estimación teórica de mercado."

    # Informe final en pantalla
    st.markdown(f"### 📊 Resultado del Análisis: **{marca_final} {modelo_final}** ({potencia_cv} CV - {combustible} - {transmisión})")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Valor Teórico Estimado", f"{formato_es(valor_mercado_ajustado)} €")
    m2.metric("Precio al Contado", f"{formato_es(precio_contado)} €")
    m3.metric("Desviación de Mercado", f"{variacion_pct:+.1f}%".replace(".", ","))
    
    # Si financia, mostramos métrica extra del sobrecoste de la financiación
    if tiene_financiacion and precio_financiado > 0:
        sobrecoste_financiacion = precio_financiado - precio_contado
        st.markdown("---")
        col_f1, col_f2 = st.columns(2)
        col_f1.metric("Precio Total Financiado", f"{formato_es(precio_financiado)} €")
        col_f2.metric("Sobrecoste por Financiar (Intereses/Comisiones)", f"+ {formato_es(sobrecoste_financiacion)} €", delta_color="inverse")
        if sobrecoste_financiacion > 2000:
            st.warning(f"⚠️ **Aviso de Financiación:** Estás pagando **{formato_es(sobrecoste_financiacion)} € extra** sobre el precio al contado. Valora si los descuentos aplicados por financiar compensan este sobrecoste.")

    st.markdown(f"#### Veredicto: {estado}")
    st.info(f"**Justificación:** {detalle}")

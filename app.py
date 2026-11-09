import streamlit as st
import datetime

st.set_page_config(page_title="Analizador Inteligente de Precios de Coches de Ocasión", layout="wide")

st.title("🚗 Analizador Inteligente de Precios de Coches de Ocasión")

# Base de datos completa con marcas, modelos y especificaciones técnicas orientativas
BASE_DATOS_COCHES = {
    "Toyota": {
        "Yaris": {"precio_nuevo": 21500, "potencia": 116, "combustible": "Híbrido", "transmisión": "Automática"},
        "Corolla": {"precio_nuevo": 26000, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "C-HR": {"precio_nuevo": 31000, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "RAV4": {"precio_nuevo": 39000, "potencia": 218, "combustible": "Híbrido", "transmisión": "Automática"},
        "Camry": {"precio_nuevo": 42000, "potencia": 218, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Honda": {
        "Civic": {"precio_nuevo": 32000, "potencia": 184, "combustible": "Híbrido", "transmisión": "Automática"},
        "HR-V": {"precio_nuevo": 33000, "potencia": 131, "combustible": "Híbrido", "transmisión": "Automática"},
        "CR-V": {"precio_nuevo": 42000, "potencia": 184, "combustible": "Híbrido", "transmisión": "Automática"},
        "Jazz": {"precio_nuevo": 24000, "potencia": 109, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Volkswagen": {
        "Polo": {"precio_nuevo": 21000, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Golf": {"precio_nuevo": 31000, "potencia": 130, "combustible": "Gasolina", "transmisión": "Manual"},
        "T-Roc": {"precio_nuevo": 28000, "potencia": 115, "combustible": "Gasolina", "transmisión": "Manual"},
        "Tiguan": {"precio_nuevo": 38000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
        "Passat": {"precio_nuevo": 40000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"}
    },
    "Seat": {
        "Ibiza": {"precio_nuevo": 19000, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Leon": {"precio_nuevo": 24500, "potencia": 110, "combustible": "Gasolina", "transmisión": "Manual"},
        "Arona": {"precio_nuevo": 22000, "potencia": 110, "combustible": "Gasolina", "transmisión": "Manual"},
        "Ateca": {"precio_nuevo": 28000, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Tarraco": {"precio_nuevo": 35000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"}
    },
    "Renault": {
        "Clio": {"precio_nuevo": 18000, "potencia": 90, "combustible": "Gasolina", "transmisión": "Manual"},
        "Captur": {"precio_nuevo": 23000, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "Megane": {"precio_nuevo": 26000, "potencia": 140, "combustible": "Híbrido", "transmisión": "Automática"},
        "Austral": {"precio_nuevo": 32000, "potencia": 200, "combustible": "Híbrido", "transmisión": "Automática"},
        "Arkana": {"precio_nuevo": 29000, "potencia": 145, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Peugeot": {
        "208": {"precio_nuevo": 18500, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "2008": {"precio_nuevo": 24000, "potencia": 130, "combustible": "Gasolina", "transmisión": "Automática"},
        "308": {"precio_nuevo": 26000, "potencia": 130, "combustible": "Gasolina", "transmisión": "Manual"},
        "3008": {"precio_nuevo": 33000, "potencia": 130, "combustible": "Diésel", "transmisión": "Automática"},
        "5008": {"precio_nuevo": 38000, "potencia": 130, "combustible": "Diésel", "transmisión": "Automática"}
    },
    "Ford": {
        "Fiesta": {"precio_nuevo": 18000, "potencia": 95, "combustible": "Gasolina", "transmisión": "Manual"},
        "Focus": {"precio_nuevo": 26000, "potencia": 125, "combustible": "Gasolina", "transmisión": "Manual"},
        "Puma": {"precio_nuevo": 24000, "potencia": 125, "combustible": "Híbrido", "transmisión": "Manual"},
        "Kuga": {"precio_nuevo": 32000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Hyundai": {
        "i20": {"precio_nuevo": 17500, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "i30": {"precio_nuevo": 23000, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Kona": {"precio_nuevo": 25000, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Tucson": {"precio_nuevo": 31000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Santa Fe": {"precio_nuevo": 45000, "potencia": 230, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Kia": {
        "Picanto": {"precio_nuevo": 14000, "potencia": 67, "combustible": "Gasolina", "transmisión": "Manual"},
        "Ceed": {"precio_nuevo": 22000, "potencia": 120, "combustible": "Gasolina", "transmisión": "Manual"},
        "Stonic": {"precio_nuevo": 21000, "potencia": 100, "combustible": "Gasolina", "transmisión": "Manual"},
        "Sportage": {"precio_nuevo": 31000, "potencia": 150, "combustible": "Híbrido", "transmisión": "Automática"},
        "Sorento": {"precio_nuevo": 44000, "potencia": 230, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "BMW": {
        "Serie 1": {"precio_nuevo": 32000, "potencia": 136, "combustible": "Gasolina", "transmisión": "Automática"},
        "Serie 3": {"precio_nuevo": 43000, "potencia": 184, "combustible": "Diésel", "transmisión": "Automática"},
        "Serie 5": {"precio_nuevo": 58000, "potencia": 190, "combustible": "Diésel", "transmisión": "Automática"},
        "X1": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
        "X3": {"precio_nuevo": 54000, "potencia": 190, "combustible": "Híbrido", "transmisión": "Automática"},
        "X5": {"precio_nuevo": 78000, "potencia": 286, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Mercedes-Benz": {
        "Clase A": {"precio_nuevo": 33000, "potencia": 136, "combustible": "Gasolina", "transmisión": "Automática"},
        "Clase C": {"precio_nuevo": 47000, "potencia": 200, "combustible": "Híbrido", "transmisión": "Automática"},
        "Clase E": {"precio_nuevo": 60000, "potencia": 197, "combustible": "Diésel", "transmisión": "Automática"},
        "GLA": {"precio_nuevo": 40000, "potencia": 150, "combustible": "Diésel", "transmisión": "Automática"},
        "GLC": {"precio_nuevo": 59000, "potencia": 197, "combustible": "Híbrido", "transmisión": "Automática"}
    },
    "Audi": {
        "A3": {"precio_nuevo": 31000, "potencia": 116, "combustible": "Gasolina", "transmisión": "Manual"},
        "A4": {"precio_nuevo": 42000, "potencia": 163, "combustible": "Diésel", "transmisión": "Automática"},
        "A6": {"precio_nuevo": 57000, "potencia": 204, "combustible": "Diésel", "transmisión": "Automática"},
        "Q3": {"precio_nuevo": 39000, "potencia": 150, "combustible": "Gasolina", "transmisión": "Automática"},
        "Q5": {"precio_nuevo": 53000, "potencia": 204, "combustible": "Diésel", "transmisión": "Automática"}
    }
}

st.markdown("### 📋 Datos del Vehículo y Financiación")

col_m1, col_m2 = st.columns(2)

with col_m1:
    # --- SELECCIÓN DE MARCA ---
    opciones_marcas = ["-- Selecciona o escribe abajo --"] + sorted(list(BASE_DATOS_COCHES.keys()))
    marca_sel = st.selectbox("Marca del Vehículo", options=opciones_marcas)
    marca_man = st.text_input("¿Otra marca? Escríbela aquí:", value="").strip()
    
    marca_final = marca_man.strip().title() if marca_man else (marca_sel if not marca_sel.startswith("--") else "Marca no especificada")

    # --- SELECCIÓN DE MODELO ---
    modelos_disponibles = list(BASE_DATOS_COCHES.get(marca_final, {}).keys())
    opciones_modelos = ["-- Selecciona o escribe abajo --"] + modelos_disponibles
    
    modelo_sel = st.selectbox("Modelo del Vehículo", options=opciones_modelos)
    modelo_man = st.text_input("¿Otro modelo? Escríbela aquí:", value="").strip()
    
    modelo_final = modelo_man.strip().title() if modelo_man else (modelo_sel if not modelo_sel.startswith("--") else "Modelo no especificado")

    # Valores por defecto por si no se encuentra en la base de datos
    precio_sugerido = 25000.0
    potencia_sugerida = 110
    combustible_sugerido = "Gasolina"
    transmision_sugerida = "Manual"

    # Autocompletar si existe en la base de datos
    if marca_final in BASE_DATOS_COCHES and modelo_final in BASE_DATOS_COCHES[marca_final]:
        datos_auto = BASE_DATOS_COCHES[marca_final][modelo_final]
        precio_sugerido = float(datos_auto["precio_nuevo"])
        potencia_sugerida = int(datos_auto["potencia"])
        combustible_sugerido = datos_auto["combustible"]
        transmision_sugerida = datos_auto["transmisión"]

    precio_nuevo = st.number_input("Precio de Venta Nuevo Original (€)", min_value=0.0, value=precio_sugerido, step=500.0, format="%.2f")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        potencia_cv = st.number_input("Potencia (CV)", min_value=30, max_value=1000, value=potencia_sugerida, step=5)
    with col_t2:
        lista_transmisiones = ["Manual", "Automática"]
        idx_trans = lista_transmisiones.index(transmision_sugerida) if transmision_sugerida in lista_transmisiones else 0
        transmision = st.selectbox("Transmisión", lista_transmisiones, index=idx_trans)
        
    lista_combustibles = ["Gasolina", "Diésel", "Híbrido", "Híbrido Enchufe (PHEV)", "Eléctrico (EV)", "GLP / GNC"]
    idx_comb = lista_combustibles.index(combustible_sugerido) if combustible_sugerido in lista_combustibles else 0
    combustible = st.selectbox("Tipo de Combustión", lista_combustibles, index=idx_comb)

with col_m2:
    ano_matriculacion = st.number_input("Año de Matriculación", min_value=1980, max_value=datetime.datetime.now().year, value=2020, step=1)
    km_actuales = st.number_input("Kilometraje Actual (km)", min_value=0, value=75000, step=5000)
    
    precio_contado = st.number_input("Precio al Contado (€)", min_value=0.0, value=14500.0, step=500.0, format="%.2f")
    
    # --- BLOQUE DE FINANCIACIÓN DESGLOSADO ---
    tiene_financiacion = st.checkbox("¿Tiene opción o precio financiado?")
    precio_financiado = 0.0
    entrada_dinero = 0.0
    cuota_mensual = 0.0
    num_cuotas = 0
    precio_financiado_total = 0.0

    if tiene_financiacion:
        st.markdown("##### 💳 Desglose de la Financiación")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            entrada_dinero = st.number_input("Entrada (€)", min_value=0.0, value=3000.0, step=500.0, format="%.2f")
        with col_f2:
            cuota_mensual = st.number_input("Cuota Mensual (€/mes)", min_value=0.0, value=230.0, step=10.0, format="%.2f")
        with col_f3:
            num_cuotas = st.number_input("Número de Cuotas (meses)", min_value=1, max_value=120, value=60, step=6)
        
        # Cálculo automático del precio total financiado
        precio_financiado_total = entrada_dinero + (cuota_mensual * num_cuotas)
        st.caption(f"💰 **Precio Total Financiado:** {entrada_dinero:,.2f}€ (Entrada) + ({cuota_mensual:,.2f}€ × {num_cuotas} meses) = **{precio_financiado_total:,.2f}€**".replace(",", "X").replace(".", ",").replace("X", "."))

    etiqueta_dgt = st.selectbox("Etiqueta Ambiental DGT", ["ECO / Cero", "C", "B", "Sin Etiqueta"])

st.markdown("---")

def formato_es(valor):
    """Convierte un número a formato español: puntos para miles y coma para decimales"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if st.button("Analizar si está Barato, Correcto o Caro", type="primary", use_container_width=True):
    # 1. Cálculo de edad exacta
    ano_actual = datetime.datetime.now().year
    edad_anos = max(1, ano_actual - ano_matriculacion)
    
    # 2. Curva de depreciación base + factor corrector por tipo de combustible
    corrector_combustible = 1.0
    if combustible in ["Híbrido", "Eléctrico (EV)", "Híbrido Enchufe (PHEV)"]:
        corrector_combustible = 1.03  
        
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
    st.markdown(f"### 📊 Resultado del Análisis: **{marca_final} {modelo_final}** ({potencia_cv} CV - {combustible} - {transmision})")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Valor Teórico Estimado", f"{formato_es(valor_mercado_ajustado)} €")
    m2.metric("Precio al Contado", f"{formato_es(precio_contado)} €")
    m3.metric("Desviación de Mercado", f"{variacion_pct:+.1f}%".replace(".", ","))
    
    # --- RESULTADOS DE FINANCIACIÓN DESGLOSADOS ---
    if tiene_financiacion and precio_financiado_total > 0:
        sobrecoste_financiacion = precio_financiado_total - precio_contado
        st.markdown("---")
        st.markdown("### 💳 Análisis de la Financiación")
        
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Entrada Inicial", f"{formato_es(entrada_dinero)} €")
        f2.metric("Cuota Mensual", f"{formato_es(cuota_mensual)} € / mes", delta=f"{num_cuotas} meses", delta_color="off")
        f3.metric("Total Financiado", f"{formato_es(precio_financiado_total)} €")
        f4.metric("Sobrecoste (Intereses/Comisiones)", f"+ {formato_es(sobrecoste_financiacion)} €", delta_color="inverse")
        
        if sobrecoste_financiacion > 2000:
            st.warning(f"⚠️ **Aviso de Financiación:** Al financiar pagas **{formato_es(sobrecoste_financiacion)} € más** que al contado. Comprueba si los descuentos de la oferta compensan los intereses totales.")

    st.markdown(f"#### Veredicto: {estado}")
    st.info(f"**Justificación:** {detalle}")

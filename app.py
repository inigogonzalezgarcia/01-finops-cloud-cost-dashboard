# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from data_generator import generate_finops_data

# Configuración de página
st.set_page_config(
    page_title="FinOps Cloud Cost & Anomalies Dashboard",
    page_icon="☁️",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main { padding: 1.5rem; }
    .stMetric { background-color: #f8f9fa; padding: 10px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Cargar Datos (Cacheado)
@st.cache_data
def load_data():
    return generate_finops_data()

df = load_data()

# Header Principal
st.title("☁️ Multi-Cloud FinOps & Cost Optimization Dashboard")
st.caption("Herramienta de monitorización de costes cloud y detección de anomalías en tiempo real.")

# Barra Lateral: Filtros
st.sidebar.header("🔍 Filtros de Infraestructura")
selected_provider = st.sidebar.multiselect("Proveedor Cloud", options=df["Provider"].unique(), default=df["Provider"].unique())
selected_env = st.sidebar.multiselect("Entorno", options=df["Environment"].unique(), default=df["Environment"].unique())
selected_dept = st.sidebar.multiselect("Departamento", options=df["Department"].unique(), default=df["Department"].unique())

# Filtrar DataFrame
filtered_df = df[
    (df["Provider"].isin(selected_provider)) &
    (df["Environment"].isin(selected_env)) &
    (df["Department"].isin(selected_dept))
]

# Métricas Clave (KPIs)
total_cost = filtered_df["Cost_USD"].sum()
recent_7_days = filtered_df[filtered_df["Date"] >= (filtered_df["Date"].max() - pd.Timedelta(days=7))]["Cost_USD"].sum()
prev_7_days = filtered_df[
    (filtered_df["Date"] < (filtered_df["Date"].max() - pd.Timedelta(days=7))) &
    (filtered_df["Date"] >= (filtered_df["Date"].max() - pd.Timedelta(days=14)))
]["Cost_USD"].sum()

delta_weekly = ((recent_7_days - prev_7_days) / prev_7_days) * 100 if prev_7_days > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gasto Total Acumulado", f"${total_cost:,.2f}")
col2.metric("Gasto Últimos 7 Días", f"${recent_7_days:,.2f}", f"{delta_weekly:.1f}% vs sem. anterior", delta_color="inverse")
col3.metric("Proveedores Activos", f"{len(selected_provider)}")
col4.metric("Entornos Evaluados", f"{len(selected_env)}")

st.divider()

# Gráficos Principales
g1, g2 = st.columns([2, 1])

with g1:
    st.subheader("📈 Tendencia Diaria de Gasto por Proveedor")
    daily_cost = filtered_df.groupby(["Date", "Provider"])["Cost_USD"].sum().reset_index()
    fig_line = px.line(
        daily_cost, x="Date", y="Cost_USD", color="Provider",
        title="Gasto diario (USD)", labels={"Cost_USD": "Gasto ($)"},
        color_discrete_map={"AWS": "#FF9900", "Azure": "#0089D6"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

with g2:
    st.subheader("📊 Distribución por Entorno")
    env_cost = filtered_df.groupby("Environment")["Cost_USD"].sum().reset_index()
    fig_pie = px.pie(env_cost, values="Cost_USD", names="Environment", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Sección FinOps: Detección de Anomalías
st.subheader("⚠️ Recomendaciones FinOps y Detección de Anomalías")

# Lógica de detección de anomalías simple
recent_dev_ec2 = filtered_df[
    (filtered_df["Provider"] == "AWS") &
    (filtered_df["Service"] == "EC2") &
    (filtered_df["Environment"] == "Development") &
    (filtered_df["Date"] >= (filtered_df["Date"].max() - pd.Timedelta(days=7)))
]

if not recent_dev_ec2.empty:
    st.error("""
    **Anomalía Detectada (AWS EC2 - Development):** Se detectó un pico inusual de gasto (+280%) en instancias EC2 del entorno de Desarrollo en los últimos 7 días.
    * **Causa probable:** Instancias de pruebas no apagadas durante el fin de semana.
    * **Acción sugerida:** Implementar políticas de Auto-Shutdown o Terraform Lifecycle Rules para reducir hasta $2,400/mes.
    """)
else:
    st.success("No se han detectado anomalías de sobrecoste críticas en los filtros seleccionados.")

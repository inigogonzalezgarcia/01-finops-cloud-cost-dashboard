# 01. FinOps Cloud Cost & Anomalies Dashboard

Este proyecto es un Dashboard interactivo de **FinOps y Optimización de Costes Cloud** enfocado en entornos híbridos (AWS/Azure). Permite a líderes de IT supervisar el gasto, analizar tendencias por departamento/entorno y detectar picos inusuales de costes causados por recursos desatendidos.

## 🏗️ Arquitectura
```mermaid
graph TD
    A[Cloud Infrastructure AWS / Azure] -->|Billing Data / Metrics| B[Python Engine Pandas]
    B -->|Anomaly Detection Logic| C[FinOps Rules Engine]
    B -->|Aggregated Data| D[Streamlit Dashboard UI]
    C -->|Alerts & Recommendations| D

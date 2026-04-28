"""
LATINNOVA — Dashboard de Pipeline de IA
Página principal con KPIs globales, evolución de métricas y estado del sistema.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Latinnova — Pipeline IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# CSS corporativo: azul oscuro #1E3A5F / rojo #E74C3C
# ------------------------------------------------------------------
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1E3A5F; }
  [data-testid="stSidebar"] * { color: #FFFFFF !important; }
  .main-header {
      background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
      padding: 1.5rem 2rem;
      border-radius: 12px;
      margin-bottom: 1.5rem;
      color: white;
  }
  .status-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
  }
  .badge-ok   { background: #27AE60; color: white; }
  .badge-mock { background: #F39C12; color: white; }
  .badge-err  { background: #E74C3C; color: white; }
  .metric-card {
      background: #F8F9FA;
      border-left: 4px solid #1E3A5F;
      border-radius: 8px;
      padding: 1rem;
  }
  .section-title {
      color: #1E3A5F;
      font-size: 1.2rem;
      font-weight: 700;
      margin: 1.5rem 0 0.5rem 0;
      border-bottom: 2px solid #E74C3C;
      padding-bottom: 4px;
  }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Importar cliente y detectar modo mock
# ------------------------------------------------------------------
from utils.n8n_client import get_client, safe_json_parse, _load_credentials
_url, _key, _webhook = _load_credentials()
using_mock = not (_key and _url and "localhost" not in _url)

client = get_client()

# ------------------------------------------------------------------
# Header principal
# ------------------------------------------------------------------
badge_html = (
    '<span class="status-badge badge-mock">⚠ Modo Demo (Mock)</span>'
    if using_mock
    else '<span class="status-badge badge-ok">✅ Conectado a n8n</span>'
)

st.markdown(f"""
<div class="main-header">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <h1 style="margin:0; font-size:2rem;">🔬 LATINNOVA</h1>
      <p style="margin:0; opacity:0.85; font-size:1.05rem;">
        Modelo basado en inteligencia artificial para la priorización automática de oportunidades a partir del análisis de convocatorias de proyectos de innovación
      </p>
    </div>
    <div>{badge_html}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Botón de refresco
# ------------------------------------------------------------------
col_refresh, _ = st.columns([1, 5])
with col_refresh:
    if st.button("🔄 Refrescar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ------------------------------------------------------------------
# Carga de datos
# ------------------------------------------------------------------
with st.spinner("Cargando datos..."):
    df_exp    = client.get_table("experiment_log")
    df_eval   = client.get_table("evaluation_results")
    df_runs   = client.get_table("pipeline_runs")
    df_match  = client.get_table("resultados_match")
    df_jobs   = client.get_table("linkedin_jobs")

# ------------------------------------------------------------------
# KPIs globales
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📊 KPIs Globales</p>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_jobs = len(df_jobs)
total_matches = int(df_match["total_matches_aplicar"].sum()) if not df_match.empty and "total_matches_aplicar" in df_match.columns else 0
best_f1 = round(df_exp["f1"].max(), 3) if not df_exp.empty and "f1" in df_exp.columns else 0.0
last_exp = df_exp["experiment_id"].iloc[-1] if not df_exp.empty else "N/A"

with kpi1:
    st.metric("📋 Oportunidades procesadas", total_jobs, help="Total de LinkedIn jobs clasificados")

with kpi2:
    st.metric("🎯 Matches 'Aplicar'", total_matches, help="Total de matches con decisión 'aplicar'")

with kpi3:
    st.metric("🏆 Mejor F1-Score", f"{best_f1:.3f}", help="F1 máximo entre todos los experimentos")

with kpi4:
    st.metric("🧪 Último experimento", last_exp, help="ID del experimento más reciente")

# ------------------------------------------------------------------
# Gráfico: Evolución Precision / Recall / F1
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📈 Evolución de Métricas por Experimento</p>', unsafe_allow_html=True)

if not df_exp.empty and all(c in df_exp.columns for c in ["experiment_id", "precision", "recall", "f1"]):
    df_plot = df_exp.sort_values("experiment_id")

    fig_metrics = go.Figure()
    fig_metrics.add_trace(go.Scatter(
        x=df_plot["experiment_id"], y=df_plot["precision"],
        name="Precision", mode="lines+markers",
        line=dict(color="#4A9EE8", width=3),
        marker=dict(size=10, symbol="circle"),
    ))
    fig_metrics.add_trace(go.Scatter(
        x=df_plot["experiment_id"], y=df_plot["recall"],
        name="Recall", mode="lines+markers",
        line=dict(color="#E74C3C", width=3),
        marker=dict(size=10, symbol="square"),
    ))
    fig_metrics.add_trace(go.Scatter(
        x=df_plot["experiment_id"], y=df_plot["f1"],
        name="F1-Score", mode="lines+markers",
        line=dict(color="#27AE60", width=3, dash="dash"),
        marker=dict(size=10, symbol="diamond"),
    ))
    fig_metrics.update_layout(
        yaxis=dict(color="white", range=[0, 1.1], title="Valor de la métrica", tickformat=".2f"),
        xaxis=dict(color="white", title="Experimento"),
        legend=dict(orientation="h", y=-0.2, font=dict(color="white")),
        height=380,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(t=20, b=60),
        hovermode="x unified",
    )
    fig_metrics.update_xaxes(showgrid=True, gridcolor="#333333")
    fig_metrics.update_yaxes(showgrid=True, gridcolor="#333333")
    st.plotly_chart(fig_metrics, use_container_width=True)
else:
    st.info("Sin datos de experimentos disponibles.")

# ------------------------------------------------------------------
# Dos columnas: pipeline runs + distribución de oportunidades
# ------------------------------------------------------------------
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<p class="section-title">⚙️ Últimas Ejecuciones del Pipeline</p>', unsafe_allow_html=True)
    if not df_runs.empty:
        df_runs_display = df_runs.copy()
        if "status" in df_runs_display.columns:
            df_runs_display["Estado"] = df_runs_display["status"].map({
                "success": "✅ Success",
                "error":   "❌ Error",
                "running": "🔄 Running",
            }).fillna(df_runs_display["status"])

        cols_show = []
        col_map = {
            "run_id": "Run ID",
            "workflow_name": "Workflow",
            "Estado": "Estado",
            "model_name": "Modelo",
            "errors_count": "Errores",
            "started_at": "Inicio",
        }
        for k, v in col_map.items():
            if k in df_runs_display.columns:
                df_runs_display[v] = df_runs_display[k]
                cols_show.append(v)

        st.dataframe(
            df_runs_display[cols_show].tail(10),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Sin datos de pipeline runs.")

with col_right:
    st.markdown('<p class="section-title">🗂️ Distribución por Tipo</p>', unsafe_allow_html=True)
    if not df_jobs.empty and "tipo_oportunidad" in df_jobs.columns:
        tipo_counts = df_jobs["tipo_oportunidad"].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "Cantidad"]

        COLOR_MAP = {
            "consultoría":    "#1E3A5F",
            "empleo":         "#2C5282",
            "financiamiento": "#E74C3C",
            "evento":         "#F39C12",
            "formación":      "#27AE60",
            "otro":           "#95A5A6",
        }
        colors = [COLOR_MAP.get(t, "#999999") for t in tipo_counts["Tipo"]]

        fig_pie = go.Figure(go.Pie(
            labels=tipo_counts["Tipo"],
            values=tipo_counts["Cantidad"],
            marker_colors=colors,
            hole=0.4,
            textinfo="label+percent",
        ))
        fig_pie.update_layout(
            height=320,
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sin datos de oportunidades.")

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.divider()
st.caption(
    "Latinnova Pipeline Dashboard · "
    f"Fuente de datos: {'📦 Mock (desarrollo)' if using_mock else '🔗 n8n DataTable'} · "
    "Maestría en Inteligencia Artificial Aplicada"
)

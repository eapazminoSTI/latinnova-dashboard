"""
Página: Análisis de Experimentos
Comparativa de métricas, radar chart, matriz de confusión y análisis IA.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from utils.n8n_client import get_client


def clean_text(value) -> str:
    """Limpia campos que vienen como JSON array ["texto"] o string "texto"."""
    if not value or value == "N/A":
        return str(value)
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    text = str(value).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return " ".join(str(v) for v in parsed)
        if isinstance(parsed, str):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return text

st.set_page_config(page_title="Experimentos — Latinnova", layout="wide", page_icon="🧪")

st.markdown("""
<style>
  .section-title {
      color: #1E3A5F; font-size: 1.2rem; font-weight: 700;
      border-bottom: 2px solid #E74C3C; padding-bottom: 4px;
      margin: 1.2rem 0 0.6rem 0;
  }
  .analysis-box {
      background: #000000; border-left: 4px solid #E74C3C;
      border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem;
      color: #FFFFFF;
  }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Análisis de Experimentos")
st.caption("Comparativa de configuraciones de prompt y sus métricas de evaluación.")

client = get_client()

# ------------------------------------------------------------------
# Carga de datos
# ------------------------------------------------------------------
df_exp  = client.get_table("experiment_log")
df_eval = client.get_table("evaluation_results")
df_snap = client.get_table("dataset_snapshots")

if df_exp.empty:
    st.warning("Sin datos de experimentos.")
    st.stop()

# ------------------------------------------------------------------
# Tabla comparativa
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📊 Tabla Comparativa de Experimentos</p>', unsafe_allow_html=True)

display_cols = {
    "experiment_id": "Experimento",
    "prompt_hash": "Prompt",
    "precision": "Precisión",
    "recall": "Recall",
    "f1": "F1-Score",
    "total_pares_evaluados": "Pares eval.",
    "fecha_ejecucion": "Fecha",
}
avail = [k for k in display_cols if k in df_exp.columns]
df_table = df_exp[avail].rename(columns=display_cols)

for col in ["Precisión", "Recall", "F1-Score"]:
    if col in df_table.columns:
        df_table[col] = df_table[col].round(3)

st.dataframe(
    df_table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Precisión":  st.column_config.ProgressColumn("Precisión", min_value=0, max_value=1),
        "Recall":     st.column_config.ProgressColumn("Recall",    min_value=0, max_value=1),
        "F1-Score":   st.column_config.ProgressColumn("F1-Score",  min_value=0, max_value=1),
    },
)

# ------------------------------------------------------------------
# Selector de experimentos a comparar
# ------------------------------------------------------------------
exp_ids = df_exp["experiment_id"].tolist() if "experiment_id" in df_exp.columns else []
selected_exps = st.multiselect(
    "Seleccionar experimentos para comparar en radar",
    exp_ids,
    default=exp_ids,
)

# ------------------------------------------------------------------
# Gráfico Radar
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🕸️ Comparativa Radar (Precision / Recall / F1)</p>', unsafe_allow_html=True)

if selected_exps and all(c in df_exp.columns for c in ["precision", "recall", "f1"]):
    df_radar = df_exp[df_exp["experiment_id"].isin(selected_exps)]

    categories = ["Precision", "Recall", "F1-Score"]
    COLORS = ["#1E3A5F", "#E74C3C", "#27AE60", "#F39C12"]

    fig_radar = go.Figure()
    for i, (_, row) in enumerate(df_radar.iterrows()):
        vals = [row.get("precision", 0), row.get("recall", 0), row.get("f1", 0)]
        vals_closed = vals + [vals[0]]  # cerrar el polígono
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=categories + [categories[0]],
            fill="toself",
            name=row.get("experiment_id", f"exp_{i}"),
            line_color=COLORS[i % len(COLORS)],
            opacity=0.7,
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        height=400,
        margin=dict(t=30, b=30),
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("Selecciona al menos un experimento.")

# ------------------------------------------------------------------
# Gráfico: TP / FP / FN / TN por experimento
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📉 Matriz de Confusión por Experimento</p>', unsafe_allow_html=True)

if not df_eval.empty and all(c in df_eval.columns for c in ["experiment_id", "tp", "fp", "fn", "tn"]):
    df_eval_plot = df_eval[df_eval["experiment_id"].isin(selected_exps)] if selected_exps else df_eval

    fig_conf = go.Figure()
    for metric, color, label in [
        ("tp", "#27AE60", "TP (Verdadero Positivo)"),
        ("fp", "#E74C3C", "FP (Falso Positivo)"),
        ("fn", "#F39C12", "FN (Falso Negativo)"),
        ("tn", "#95A5A6", "TN (Verdadero Negativo)"),
    ]:
        fig_conf.add_trace(go.Bar(
            name=label,
            x=df_eval_plot["experiment_id"],
            y=df_eval_plot[metric],
            marker_color=color,
            text=df_eval_plot[metric],
            textposition="inside",
        ))

    fig_conf.update_layout(
        barmode="group",
        height=380,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(t=20, b=20),
        legend=dict(orientation="h", y=-0.25, font=dict(color="white")),
        yaxis=dict(title="Cantidad de pares", color="white", gridcolor="#333333"),
        xaxis=dict(title="Experimento", color="white"),
    )
    st.plotly_chart(fig_conf, use_container_width=True)
else:
    st.info("Sin datos de evaluación para los experimentos seleccionados.")

# ------------------------------------------------------------------
# Sección Análisis IA
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🤖 Análisis IA por Experimento</p>', unsafe_allow_html=True)

if not df_eval.empty and "experiment_id" in df_eval.columns:
    selected_exp_detail = st.selectbox(
        "Seleccionar experimento para ver análisis completo",
        df_eval["experiment_id"].tolist(),
        index=len(df_eval) - 1,
    )
    row_eval = df_eval[df_eval["experiment_id"] == selected_exp_detail].iloc[0]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Resumen", "✅ Fortalezas", "⚠️ Debilidades", "💡 Recomendaciones", "🎓 Conclusión"
    ])

    with tab1:
        st.markdown(f"<div class='analysis-box'>{clean_text(row_eval.get('resumen_ejecutivo', 'N/A'))}</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div class='analysis-box'>{clean_text(row_eval.get('fortalezas', 'N/A'))}</div>", unsafe_allow_html=True)
    with tab3:
        st.markdown(f"<div class='analysis-box'>{clean_text(row_eval.get('debilidades', 'N/A'))}</div>", unsafe_allow_html=True)
    with tab4:
        st.markdown(f"<div class='analysis-box'>{clean_text(row_eval.get('recomendaciones', 'N/A'))}</div>", unsafe_allow_html=True)
    with tab5:
        st.markdown(f"<div class='analysis-box'>{clean_text(row_eval.get('conclusion_para_tesis', 'N/A'))}</div>", unsafe_allow_html=True)

    # Análisis completo del LLM
    with st.expander("📄 Ver análisis completo generado por GPT"):
        analisis = row_eval.get("analisis_ia", "Sin análisis disponible.")
        st.markdown(analisis)

# ------------------------------------------------------------------
# Dataset Snapshots
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📦 Snapshots de Dataset por Experimento</p>', unsafe_allow_html=True)

if not df_snap.empty:
    cols_snap = {
        "experiment_id": "Experimento",
        "prompt_hash": "Prompt",
        "total_jobs": "Jobs",
        "total_consultores": "Consultores",
        "total_pares_generados": "Pares generados",
        "fecha": "Fecha",
    }
    avail_snap = [k for k in cols_snap if k in df_snap.columns]
    st.dataframe(
        df_snap[avail_snap].rename(columns=cols_snap),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Sin datos de snapshots disponibles.")

"""
Página: Resultados de Matching
Visualiza los matches generados por el pipeline con filtros interactivos.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from utils.n8n_client import get_client, safe_json_parse

st.set_page_config(page_title="Matches — Latinnova", layout="wide", page_icon="🎯")

st.markdown("""
<style>
  .section-title {
      color: #1E3A5F; font-size: 1.2rem; font-weight: 700;
      border-bottom: 2px solid #E74C3C; padding-bottom: 4px;
      margin: 1.2rem 0 0.6rem 0;
  }
  .score-bar { height: 8px; border-radius: 4px; background: #1E3A5F; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Resultados de Matching")
st.caption("Análisis de los matches generados entre consultores y oportunidades.")

client = get_client()

# ------------------------------------------------------------------
# Carga de datos
# ------------------------------------------------------------------
df_match = client.get_table("resultados_match")

if df_match.empty:
    st.warning("No hay datos de matching disponibles.")
    st.stop()

# ------------------------------------------------------------------
# Selector de ejecución
# ------------------------------------------------------------------
if "fecha_ejecucion" in df_match.columns:
    fechas = df_match["fecha_ejecucion"].tolist()
    selected_fecha = st.selectbox("📅 Seleccionar ejecución", fechas, index=len(fechas) - 1)
    row = df_match[df_match["fecha_ejecucion"] == selected_fecha].iloc[0]
else:
    row = df_match.iloc[0]
    selected_fecha = "N/A"

# ------------------------------------------------------------------
# Parsear JSON de resultados
# ------------------------------------------------------------------
todos = safe_json_parse(row.get("todos_los_resultados"), default=[])
top10 = safe_json_parse(row.get("top_10_matches"), default=[])
dist  = safe_json_parse(row.get("distribucion_por_tipo"), default={})

df_todos = pd.DataFrame(todos) if todos else pd.DataFrame()
df_top10 = pd.DataFrame(top10) if top10 else pd.DataFrame()

# ------------------------------------------------------------------
# KPIs de la ejecución
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📊 Métricas de esta Ejecución</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
total_aplicar = int(row.get("total_matches_aplicar", 0))

scores = df_todos["score_match"].tolist() if not df_todos.empty and "score_match" in df_todos.columns else []
score_prom = round(sum(scores) / len(scores), 3) if scores else 0.0
score_max  = round(max(scores), 3) if scores else 0.0

c1.metric("🎯 Matches 'Aplicar'", total_aplicar)
c2.metric("📈 Score Promedio", f"{score_prom:.3f}")
c3.metric("🏆 Score Máximo", f"{score_max:.3f}")
c4.metric("📋 Total evaluados", len(df_todos))

# ------------------------------------------------------------------
# Filtros
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🔍 Filtros</p>', unsafe_allow_html=True)

if not df_todos.empty:
    f1, f2, f3 = st.columns(3)

    tipos_disponibles = sorted(df_todos["tipo_oportunidad"].unique().tolist()) if "tipo_oportunidad" in df_todos.columns else []
    consultores_disponibles = sorted(df_todos["nombre_consultor"].unique().tolist()) if "nombre_consultor" in df_todos.columns else []

    with f1:
        tipos_sel = st.multiselect("Tipo de oportunidad", tipos_disponibles, default=tipos_disponibles)
    with f2:
        consult_sel = st.multiselect("Consultor", consultores_disponibles, default=consultores_disponibles)
    with f3:
        score_range = st.slider("Rango de score", 0.0, 1.0, (0.0, 1.0), step=0.01)

    # Aplicar filtros
    df_filtered = df_todos.copy()
    if tipos_sel and "tipo_oportunidad" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["tipo_oportunidad"].isin(tipos_sel)]
    if consult_sel and "nombre_consultor" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["nombre_consultor"].isin(consult_sel)]
    if "score_match" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["score_match"] >= score_range[0]) &
            (df_filtered["score_match"] <= score_range[1])
        ]
else:
    df_filtered = pd.DataFrame()

# ------------------------------------------------------------------
# Tabla interactiva de resultados
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📋 Tabla de Resultados</p>', unsafe_allow_html=True)

if not df_filtered.empty:
    DECISION_ICON = {"aplicar": "✅ aplicar", "no_aplicar": "❌ no_aplicar"}

    df_display = df_filtered.copy()
    if "decision" in df_display.columns:
        df_display["decision"] = df_display["decision"].map(DECISION_ICON).fillna(df_display["decision"])
    if "score_match" in df_display.columns:
        df_display["score_match"] = df_display["score_match"].round(4)

    col_map = {
        "rank": "Rank",
        "nombre_consultor": "Consultor",
        "nombre_oportunidad": "Oportunidad",
        "tipo_oportunidad": "Tipo",
        "score_match": "Score",
        "decision": "Decisión",
    }
    cols_available = [k for k in col_map if k in df_display.columns]
    df_show = df_display[cols_available].rename(columns=col_map)

    st.dataframe(
        df_show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                help="Score de afinidad consultor-oportunidad",
                min_value=0.0,
                max_value=1.0,
            ),
        },
    )

    # Detalles expandibles por fila
    st.markdown('<p class="section-title">🔎 Detalle del Motivo (expandible)</p>', unsafe_allow_html=True)
    for _, r in df_filtered.iterrows():
        label = f"#{r.get('rank','?')} — {r.get('nombre_consultor','?')} ↔ {r.get('nombre_oportunidad','?')} (score: {r.get('score_match',0):.3f})"
        with st.expander(label):
            st.markdown(f"**Tipo:** {r.get('tipo_oportunidad', 'N/A')}")
            st.markdown(f"**Decisión:** {r.get('decision', 'N/A')}")
            st.markdown(f"**Motivo del LLM:**")
            st.info(r.get("motivo", "Sin motivo registrado."))
else:
    st.info("No hay resultados con los filtros aplicados.")

# ------------------------------------------------------------------
# Gráfico: Top 10 por score (barras horizontales)
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🏅 Top 10 Matches por Score</p>', unsafe_allow_html=True)

if not df_top10.empty and "score_match" in df_top10.columns and "nombre_consultor" in df_top10.columns:
    df_top10_sorted = df_top10.sort_values("score_match", ascending=True)
    df_top10_sorted["label"] = (
        df_top10_sorted["nombre_consultor"] + " ↔ " +
        df_top10_sorted.get("nombre_oportunidad", pd.Series(["?"] * len(df_top10_sorted))).fillna("?")
    )

    fig_top10 = go.Figure(go.Bar(
        y=df_top10_sorted["label"],
        x=df_top10_sorted["score_match"],
        orientation="h",
        marker_color="#1E3A5F",
        text=df_top10_sorted["score_match"].round(3),
        textposition="outside",
    ))
    fig_top10.update_layout(
        xaxis=dict(range=[0, 1.05], title="Score de Matching"),
        yaxis_title="",
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=60, t=20, b=20),
    )
    st.plotly_chart(fig_top10, use_container_width=True)

# ------------------------------------------------------------------
# Gráfico: Distribución por tipo
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🗂️ Distribución por Tipo de Oportunidad</p>', unsafe_allow_html=True)

col_pie, col_bar = st.columns(2)

if dist:
    labels = list(dist.keys())
    values = list(dist.values())

    COLOR_MAP = {
        "consultoría": "#1E3A5F", "empleo": "#2C5282",
        "financiamiento": "#E74C3C", "evento": "#F39C12",
        "formación": "#27AE60", "otro": "#95A5A6",
    }
    colors = [COLOR_MAP.get(l, "#999") for l in labels]

    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=labels, values=values,
            marker_colors=colors, hole=0.4,
            textinfo="label+value",
            textfont=dict(color="white"),
        ))
        fig_pie.update_layout(
            height=300,
            margin=dict(t=10, b=10),
            showlegend=False,
            paper_bgcolor="#1a1a2e",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        fig_bar = go.Figure(go.Bar(
            x=labels, y=values,
            marker_color=colors,
            text=values, textposition="outside",
            textfont=dict(color="white"),
        ))
        fig_bar.update_layout(
            height=300,
            plot_bgcolor="black",
            paper_bgcolor="black",
            margin=dict(t=10, b=20),
            yaxis=dict(title="Cantidad", color="white", gridcolor="#333333"),
            xaxis=dict(color="white"),
            font=dict(color="white"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

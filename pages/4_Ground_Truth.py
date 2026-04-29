"""
Página: Validación Humana (Ground Truth)
Muestra los pares evaluados manualmente y permite agregar nuevas evaluaciones.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import uuid
from datetime import datetime
from utils.n8n_client import get_client, safe_json_parse

st.set_page_config(page_title="Ground Truth — Latinnova", layout="wide", page_icon="✅")

st.markdown("""
<style>
  .section-title {
      color: #1E3A5F; font-size: 1.2rem; font-weight: 700;
      border-bottom: 2px solid #E74C3C; padding-bottom: 4px;
      margin: 1.2rem 0 0.6rem 0;
  }
</style>
""", unsafe_allow_html=True)

st.title("✅ Validación Humana — Ground Truth")
st.caption("Pares consultor-oportunidad evaluados manualmente por expertos del proyecto.")

client = get_client()

# ------------------------------------------------------------------
# Carga de datos
# ------------------------------------------------------------------
df_gt    = client.get_table("ground_truth")
df_exp   = client.get_table("experiment_log")
df_eval  = client.get_table("evaluation_results")
df_match = client.get_table("resultados_match")

if df_gt.empty:
    st.warning("Sin datos de ground truth disponibles.")
    st.stop()

# ------------------------------------------------------------------
# KPIs globales
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📊 Estado del Ground Truth</p>', unsafe_allow_html=True)

total_eval = len(df_gt)
total_correct = int(df_gt["es_correcto"].sum()) if "es_correcto" in df_gt.columns else 0
total_incorrect = total_eval - total_correct
pct_correct   = round((total_correct / total_eval) * 100, 1) if total_eval > 0 else 0.0
pct_incorrect = round((total_incorrect / total_eval) * 100, 1) if total_eval > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Total evaluado", total_eval)
c2.metric("✅ Correctos", total_correct, f"{pct_correct}%")
c3.metric("❌ Incorrectos", total_incorrect, f"-{pct_incorrect}%")
c4.metric("👥 Evaluadores", df_gt["evaluador"].nunique() if "evaluador" in df_gt.columns else 0)

# ------------------------------------------------------------------
# Tabla de ground truth
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📋 Tabla de Evaluaciones</p>', unsafe_allow_html=True)

df_display = df_gt.copy()
if "es_correcto" in df_display.columns:
    df_display["Resultado"] = df_display["es_correcto"].map({True: "✅ Correcto", False: "❌ Incorrecto"})

col_map = {
    "par_id": "Par ID",
    "experiment_id": "Experimento",
    "nombre_oportunidad": "Oportunidad",
    "nombre_consultor": "Consultor",
    "Resultado": "Resultado",
    "evaluador": "Evaluador",
    "comentario": "Comentario",
    "evaluated_at": "Evaluado en",
}
avail = [k for k in col_map if k in df_display.columns]
st.dataframe(
    df_display[avail].rename(columns=col_map),
    use_container_width=True,
    hide_index=True,
)

# ------------------------------------------------------------------
# Gráfico: Accuracy por experimento vs F1 calculado
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📈 Accuracy (GT) vs F1-Score por Experimento</p>', unsafe_allow_html=True)

if "experiment_id" in df_gt.columns and "es_correcto" in df_gt.columns:
    acc_por_exp = (
        df_gt.groupby("experiment_id")["es_correcto"]
        .agg(["sum", "count"])
        .reset_index()
    )
    acc_por_exp.columns = ["experiment_id", "correctos", "total"]
    acc_por_exp["accuracy"] = acc_por_exp["correctos"] / acc_por_exp["total"]

    fig_acc = go.Figure()
    fig_acc.add_trace(go.Bar(
        name="Accuracy (Ground Truth)",
        x=acc_por_exp["experiment_id"],
        y=acc_por_exp["accuracy"],
        marker_color="#1E3A5F",
        text=acc_por_exp["accuracy"].round(3),
        textposition="outside",
    ))

    # Superponer F1 si hay datos de experimentos
    if not df_eval.empty and "experiment_id" in df_eval.columns and "f1" in df_eval.columns:
        df_f1_merge = acc_por_exp.merge(
            df_eval[["experiment_id", "f1"]], on="experiment_id", how="left"
        )
        fig_acc.add_trace(go.Scatter(
            name="F1-Score (Pipeline)",
            x=df_f1_merge["experiment_id"],
            y=df_f1_merge["f1"],
            mode="lines+markers",
            line=dict(color="#E74C3C", width=3),
            marker=dict(size=10),
        ))

    fig_acc.update_layout(
        yaxis=dict(range=[0, 1.1], title="Valor", tickformat=".2f", color="white", gridcolor="#333333"),
        xaxis=dict(title="Experimento", color="white"),
        height=360,
        plot_bgcolor="black", paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(orientation="h", y=-0.25, font=dict(color="white")),
        margin=dict(t=20, b=60),
        barmode="group",
    )
    st.plotly_chart(fig_acc, use_container_width=True)

# ------------------------------------------------------------------
# Gráfico: Correctos vs Incorrectos por experimento
# ------------------------------------------------------------------
if "experiment_id" in df_gt.columns and "es_correcto" in df_gt.columns:
    df_gt_plot = df_gt.copy()
    df_gt_plot["label"] = df_gt_plot["es_correcto"].map({True: "Correcto", False: "Incorrecto"})
    pivot = df_gt_plot.groupby(["experiment_id", "label"]).size().unstack(fill_value=0)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<p class="section-title">✅/❌ Breakdown por Experimento</p>', unsafe_allow_html=True)
        fig_breakdown = go.Figure()
        if "Correcto" in pivot.columns:
            fig_breakdown.add_trace(go.Bar(name="✅ Correcto", x=pivot.index, y=pivot["Correcto"], marker_color="#27AE60"))
        if "Incorrecto" in pivot.columns:
            fig_breakdown.add_trace(go.Bar(name="❌ Incorrecto", x=pivot.index, y=pivot["Incorrecto"], marker_color="#E74C3C"))
        fig_breakdown.update_layout(
            barmode="stack", height=280,
            plot_bgcolor="black", paper_bgcolor="black",
            font=dict(color="white"),
            xaxis=dict(color="white"),
            yaxis=dict(color="white", gridcolor="#333333"),
            legend=dict(font=dict(color="white")),
            margin=dict(t=10, b=20),
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)

# ------------------------------------------------------------------
# Formulario: Agregar nueva evaluación de ground truth
# ------------------------------------------------------------------
st.markdown('<p class="section-title">➕ Agregar Nueva Evaluación</p>', unsafe_allow_html=True)

# Mensajes persistentes tras el rerun
if st.session_state.get("gt_saved"):
    st.success("✅ Evaluación guardada exitosamente en n8n.")
    del st.session_state["gt_saved"]
elif st.session_state.get("gt_warning"):
    st.warning("⚠ No se pudo guardar en n8n (modo mock activo). La evaluación se registró localmente.")
    del st.session_state["gt_warning"]

exp_ids = df_exp["experiment_id"].tolist() if not df_exp.empty and "experiment_id" in df_exp.columns else []

if not exp_ids:
    st.info("No hay experimentos registrados aún. Ejecuta al menos un experimento para poder agregar evaluaciones de ground truth.")
else:
    # Construir lista de pares únicos desde todos_los_resultados de resultados_match
    unique_pairs = []
    if not df_match.empty and "todos_los_resultados" in df_match.columns:
        seen_keys = set()
        for _, row in df_match.iterrows():
            resultados = safe_json_parse(row.get("todos_los_resultados"), [])
            if isinstance(resultados, list):
                for par in resultados:
                    key = (par.get("consultor_id", ""), par.get("oportunidad_id", ""))
                    if key not in seen_keys and any(key):
                        seen_keys.add(key)
                        decision = par.get("decision", "")
                        icon = "✅" if decision == "aplicar" else "❌"
                        unique_pairs.append({
                            "label": f"{icon} {par.get('nombre_consultor', '?')} ↔ {par.get('nombre_oportunidad', '?')} [{decision}]",
                            "consultor_id": par.get("consultor_id", ""),
                            "nombre_consultor": par.get("nombre_consultor", ""),
                            "oportunidad_id": par.get("oportunidad_id", ""),
                            "nombre_oportunidad": par.get("nombre_oportunidad", ""),
                        })

    # Selector de par FUERA del form para que al cambiar recargue y pre-complete los campos
    selected_pair = None
    if unique_pairs:
        pair_labels = ["— Ingresar manualmente —"] + [p["label"] for p in unique_pairs]
        pair_sel = st.selectbox(
            "🔗 Cargar par evaluado desde el pipeline (opcional)",
            pair_labels,
            help="Selecciona un par consultor-oportunidad ya evaluado por el pipeline para auto-completar los campos.",
        )
        if pair_sel != "— Ingresar manualmente —":
            selected_pair = next((p for p in unique_pairs if p["label"] == pair_sel), None)

    with st.form("form_ground_truth"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            exp_sel   = st.selectbox("Experimento", exp_ids)
            opp_id    = st.text_input(
                "ID de Oportunidad",
                value=selected_pair["oportunidad_id"] if selected_pair else "",
                placeholder="job_001",
            )
            opp_name  = st.text_input(
                "Nombre de Oportunidad",
                value=selected_pair["nombre_oportunidad"] if selected_pair else "",
            )
        with col_f2:
            cons_id   = st.text_input(
                "ID de Consultor",
                value=selected_pair["consultor_id"] if selected_pair else "",
                placeholder="c_001",
            )
            cons_name = st.text_input(
                "Nombre del Consultor",
                value=selected_pair["nombre_consultor"] if selected_pair else "",
            )
            evaluador = st.text_input("Evaluador", placeholder="nombre_evaluador")

        es_correcto = st.radio("¿Es un match correcto?", ["✅ Sí", "❌ No"], horizontal=True)
        comentario  = st.text_area("Comentario (opcional)")

        submitted = st.form_submit_button("💾 Guardar evaluación", use_container_width=True)

        if submitted:
            if not all([exp_sel, opp_id, opp_name, cons_id, cons_name, evaluador]):
                st.error("Por favor completa todos los campos obligatorios.")
            else:
                new_row = {
                    "par_id": f"gt_{uuid.uuid4().hex[:6]}",
                    "experiment_id": exp_sel,
                    "oportunidad_id": opp_id,
                    "consultor_id": cons_id,
                    "nombre_oportunidad": opp_name,
                    "nombre_consultor": cons_name,
                    "es_correcto": es_correcto.startswith("✅"),
                    "evaluador": evaluador,
                    "comentario": comentario,
                    "evaluated_at": datetime.utcnow().isoformat(),
                }
                success = client.insert_row("ground_truth", new_row)
                if success:
                    st.session_state["gt_saved"] = True
                    st.cache_data.clear()
                else:
                    st.session_state["gt_warning"] = True
                st.rerun()

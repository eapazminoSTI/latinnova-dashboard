"""
Página: Explorador de Oportunidades
Filtra y visualiza las oportunidades clasificadas por el pipeline.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.n8n_client import get_client

st.set_page_config(page_title="Oportunidades — Latinnova", layout="wide", page_icon="💼")

st.markdown("""
<style>
  .section-title {
      color: #1E3A5F; font-size: 1.2rem; font-weight: 700;
      border-bottom: 2px solid #E74C3C; padding-bottom: 4px;
      margin: 1.2rem 0 0.6rem 0;
  }
  .card-box {
      background: #F8F9FA; border-left: 4px solid #E74C3C;
      border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;
  }
</style>
""", unsafe_allow_html=True)

st.title("💼 Explorador de Oportunidades")
st.caption("Explora y filtra las oportunidades clasificadas por el pipeline de IA.")

client = get_client()
df = client.get_table("linkedin_jobs")

if df.empty:
    st.warning("Sin datos de oportunidades disponibles.")
    st.stop()

with st.expander("🔧 Diagnóstico — columnas disponibles en la tabla", expanded=False):
    st.write(list(df.columns))

# ------------------------------------------------------------------
# Filtros en sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Filtros")

    tipos = sorted(df["tipo_oportunidad"].unique().tolist()) if "tipo_oportunidad" in df.columns else []
    tipos_sel = st.multiselect("Tipo de oportunidad", tipos, default=tipos)

    paises = sorted(df["pais"].str.strip().str.title().unique().tolist()) if "pais" in df.columns else []
    paises_sel = st.multiselect("País", paises, default=paises)

    conf_range = st.slider(
        "Confianza de clasificación",
        0.0, 1.0, (0.0, 1.0), step=0.01,
    ) if "confianza_clasificacion" in df.columns else (0.0, 1.0)

    texto_buscar = st.text_input("🔎 Búsqueda libre (cargo / objetivo)", "")

# ------------------------------------------------------------------
# Aplicar filtros
# ------------------------------------------------------------------
df_filtered = df.copy()
# Normalizar columna pais para evitar duplicados por mayúsculas/espacios
if "pais" in df_filtered.columns:
    df_filtered["pais"] = df_filtered["pais"].str.strip().str.title()

if tipos_sel and "tipo_oportunidad" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["tipo_oportunidad"].isin(tipos_sel)]

if paises_sel and "pais" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["pais"].isin(paises_sel)]

if "confianza_clasificacion" in df_filtered.columns:
    df_filtered = df_filtered[
        (df_filtered["confianza_clasificacion"] >= conf_range[0]) &
        (df_filtered["confianza_clasificacion"] <= conf_range[1])
    ]

if texto_buscar:
    mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
    for col in ["cargo", "objetivo_del_cargo"]:
        if col in df_filtered.columns:
            mask |= df_filtered[col].str.contains(texto_buscar, case=False, na=False)
    df_filtered = df_filtered[mask]

# ------------------------------------------------------------------
# KPIs de resultados filtrados
# ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("📋 Oportunidades mostradas", len(df_filtered))
c2.metric("🌎 Países representados", df_filtered["pais"].nunique() if "pais" in df_filtered.columns else 0)

conf_prom = round(df_filtered["confianza_clasificacion"].mean(), 3) if "confianza_clasificacion" in df_filtered.columns and not df_filtered.empty else 0.0
c3.metric("🎯 Confianza promedio", f"{conf_prom:.3f}")

# ------------------------------------------------------------------
# Tabla principal
# ------------------------------------------------------------------
st.markdown('<p class="section-title">📋 Tabla de Oportunidades</p>', unsafe_allow_html=True)

col_map = {
    "cargo": "Cargo",
    "tipo_oportunidad": "Tipo",
    "ciudad": "Ciudad",
    "pais": "País",
    "fecha_limite": "Fecha límite",
    "confianza_clasificacion": "Confianza",
    "URL": "🖼️ Imagen",
}
avail = [k for k in col_map if k in df_filtered.columns]

st.dataframe(
    df_filtered[avail].rename(columns=col_map),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Confianza": st.column_config.ProgressColumn("Confianza", min_value=0, max_value=1),
        "🖼️ Imagen": st.column_config.LinkColumn("🖼️ Imagen", display_text="Ver imagen"),
    },
)

# ------------------------------------------------------------------
# Tarjetas expandibles por oportunidad
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🗂️ Detalle por Oportunidad</p>', unsafe_allow_html=True)

for _, r in df_filtered.iterrows():
    cargo = r.get("cargo", "Sin cargo")
    tipo  = r.get("tipo_oportunidad", "N/A")
    pais  = r.get("pais", "N/A")
    conf  = r.get("confianza_clasificacion", 0)

    label = f"📌 {cargo} | {tipo} | {pais} | confianza: {conf:.2f}"
    with st.expander(label):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Ciudad:** {r.get('ciudad', 'N/A')}")
            st.markdown(f"**País:** {pais}")
            st.markdown(f"**Tipo:** {tipo}")
            st.markdown(f"**Confianza:** {conf:.3f}")
            st.markdown(f"**Fecha límite:** {r.get('fecha_limite', 'N/A')}")
        with col_b:
            aplica = r.get("aplica_en", "")
            if aplica:
                st.markdown(f"**Aplicar en:** [{aplica}]({aplica})")
            imagen_url = r.get("URL", "")
            if imagen_url:
                st.link_button("🖼️ Ver imagen de la oportunidad", imagen_url)
            st.markdown(f"**Razón de clasificación:** {r.get('razon_clasificacion', 'N/A')}")

        st.markdown("**Objetivo del cargo:**")
        st.info(r.get("objetivo_del_cargo", "N/A"))
        st.markdown("**Prerrequisitos:**")
        st.warning(r.get("prerrequisitos", "N/A"))

# ------------------------------------------------------------------
# Gráficos
# ------------------------------------------------------------------
col_left, col_right = st.columns(2)

COLOR_MAP = {
    "consultoría": "#1E3A5F", "empleo": "#2C5282",
    "financiamiento": "#E74C3C", "evento": "#F39C12",
    "formación": "#27AE60", "otro": "#95A5A6",
}

with col_left:
    st.markdown('<p class="section-title">📊 Distribución por Tipo</p>', unsafe_allow_html=True)
    if "tipo_oportunidad" in df_filtered.columns and not df_filtered.empty:
        tipo_counts = df_filtered["tipo_oportunidad"].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "Cantidad"]
        colors = [COLOR_MAP.get(t, "#999") for t in tipo_counts["Tipo"]]

        fig_tipo = go.Figure(go.Bar(
            x=tipo_counts["Tipo"], y=tipo_counts["Cantidad"],
            marker_color=colors,
            text=tipo_counts["Cantidad"], textposition="outside",
        ))
        fig_tipo.update_layout(
            height=320, plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title="Cantidad", margin=dict(t=10, b=20),
        )
        st.plotly_chart(fig_tipo, use_container_width=True)
    else:
        st.info("La tabla `linkedin_jobs` en n8n no contiene la columna `tipo_oportunidad`. Esta columna se genera en el paso de clasificación del pipeline.")

with col_right:
    st.markdown('<p class="section-title">🌎 Top 10 Países</p>', unsafe_allow_html=True)
    if "pais" in df_filtered.columns and not df_filtered.empty:
        pais_counts = (
            df_filtered["pais"]
            .str.strip()
            .str.title()
            .value_counts()
            .head(10)
            .reset_index()
        )
        pais_counts.columns = ["País", "Cantidad"]

        fig_pais = go.Figure(go.Bar(
            y=pais_counts["País"], x=pais_counts["Cantidad"],
            orientation="h",
            marker_color="#1E3A5F",
            text=pais_counts["Cantidad"], textposition="outside",
        ))
        fig_pais.update_layout(
            height=320,
            plot_bgcolor="black", paper_bgcolor="black",
            font=dict(color="white"),
            xaxis=dict(title="Cantidad", color="white", gridcolor="#333333"),
            yaxis=dict(color="white"),
            margin=dict(t=10, l=10, r=40, b=20),
        )
        st.plotly_chart(fig_pais, use_container_width=True)

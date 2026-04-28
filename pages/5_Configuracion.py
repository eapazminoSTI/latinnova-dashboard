"""
Página: Configuración del Dashboard
Gestiona conexión a n8n, prueba de tablas y administración de consultores.
"""
import streamlit as st
import pandas as pd
import os
from utils.n8n_client import N8NClient, get_client, _load_credentials

st.set_page_config(page_title="Configuración — Latinnova", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
  .section-title {
      color: #1E3A5F; font-size: 1.2rem; font-weight: 700;
      border-bottom: 2px solid #E74C3C; padding-bottom: 4px;
      margin: 1.2rem 0 0.6rem 0;
  }
  .status-ok   { color: #27AE60; font-weight: 700; }
  .status-warn { color: #F39C12; font-weight: 700; }
  .status-err  { color: #E74C3C; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Configuración del Dashboard")
st.caption("Gestiona la conexión a n8n y la configuración del pipeline.")

# ------------------------------------------------------------------
# Formulario de configuración
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🔗 Conexión a n8n</p>', unsafe_allow_html=True)

st.info(
    "☁️ **Entorno cloud:** Las credenciales configuradas aquí aplican solo para "
    "esta sesión activa. Para hacerlas permanentes, actualízalas en "
    "**Streamlit Cloud → App settings → Secrets**.\n\n"
    "⚠️ **Recuerda:** Si reinicias ngrok, la URL cambiará y deberás actualizarla "
    "en Secrets para reconectar el dashboard."
)

# Leer valores actuales: st.secrets → session_state → .env/defaults
_url, _key, _webhook = _load_credentials()
current_url     = st.session_state.get("n8n_url_override", _url)
current_key     = st.session_state.get("n8n_key_override", _key)
current_webhook = st.session_state.get("n8n_webhook_override", _webhook)

with st.form("form_config"):
    col1, col2 = st.columns(2)
    with col1:
        n8n_url = st.text_input(
            "N8N_URL",
            value=current_url,
            help="URL base de tu instancia n8n (sin barra final)",
        )
        webhook_url = st.text_input(
            "WEBHOOK_BASE_URL",
            value=current_webhook,
            help="URL base para los webhooks de exportación de datos",
        )
    with col2:
        n8n_key = st.text_input(
            "N8N_API_KEY",
            value=current_key,
            type="password",
            help="API Key de n8n (visible en Settings → API Keys)",
        )

    saved = st.form_submit_button("💾 Guardar configuración", use_container_width=True)

    if saved:
        # Persistir en session_state para esta sesión activa
        st.session_state["n8n_url_override"]     = n8n_url
        st.session_state["n8n_key_override"]     = n8n_key
        st.session_state["n8n_webhook_override"] = webhook_url
        # Reiniciar cliente con nuevas credenciales
        if "n8n_client" in st.session_state:
            del st.session_state["n8n_client"]
        st.cache_data.clear()
        st.success("✅ Credenciales actualizadas para esta sesión.")

# ------------------------------------------------------------------
# Prueba de conexión
# ------------------------------------------------------------------
st.markdown('<p class="section-title">🔍 Prueba de Conexión</p>', unsafe_allow_html=True)

if st.button("🚦 Probar conexión con n8n", use_container_width=False):
    active_url = st.session_state.get("n8n_url_override", _url)
    active_key = st.session_state.get("n8n_key_override", _key)

    # Debug: muestra la respuesta cruda de la API
    with st.expander("🔬 Respuesta cruda de la API (debug)", expanded=True):
        import requests as _req
        hdrs = {
            "X-N8N-API-KEY": active_key,
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
        }

        # 1. Listar tablas
        try:
            r = _req.get(f"{active_url}/api/v1/data-tables", headers=hdrs, timeout=10)
            st.code(f"[1] GET /api/v1/data-tables\nStatus: {r.status_code}\n{r.text[:400]}", language="text")
        except Exception as ex:
            st.error(f"[1] Error: {ex}")

        # 2. Filas de Consultores (ID conocido)
        try:
            r2 = _req.get(f"{active_url}/api/v1/data-tables/NdmwL0uqhJpjHCD6/rows?limit=2", headers=hdrs, timeout=10)
            st.code(f"[2] GET /api/v1/data-tables/NdmwL0uqhJpjHCD6/rows?limit=2\nStatus: {r2.status_code}\n{r2.text[:800]}", language="text")
        except Exception as ex:
            st.error(f"[2] Error rows: {ex}")

    test_client = N8NClient(base_url=active_url, api_key=active_key)
    with st.spinner("Probando conexión..."):
        results = test_client.test_connection()

    col_api, col_wh = st.columns(2)
    with col_api:
        if results.get("api_key_valid"):
            st.success("✅ API n8n: conectado y autenticado")
        elif results.get("api_reachable"):
            st.warning("⚠ API n8n: alcanzable pero API key inválida")
        else:
            st.error("❌ API n8n: no accesible")
            if "api_error" in results:
                st.caption(f"Error: {results['api_error']}")
    with col_wh:
        if results.get("webhook_reachable"):
            st.success("✅ Webhook: accesible")
        else:
            st.warning("⚠ Webhook: no accesible (se usará mock)")

    # Estado de cada tabla
    st.markdown("**Estado de tablas:**")
    tables_data = results.get("tables", {})
    if tables_data:
        rows = []
        for table_name, info in tables_data.items():
            source = info.get("source", "mock")
            rows_count = info.get("rows", 0)
            ok = info.get("ok", False)

            icon = "✅" if source == "api_directa" else ("🔶" if source == "webhook" else "📦")
            source_label = {
                "api_directa": "API Directa",
                "webhook": "Webhook",
                "mock": "Mock (desarrollo)",
            }.get(source, source)

            rows.append({
                "Tabla": table_name,
                "Fuente": f"{icon} {source_label}",
                "Filas": rows_count,
                "Estado": "✅ Activo" if ok else "📦 Mock",
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------
# Consultores activos
# ------------------------------------------------------------------
st.markdown('<p class="section-title">👥 Consultores Activos</p>', unsafe_allow_html=True)

client = get_client()
df_cons = client.get_table("Consultores")

if not df_cons.empty:
    df_cons_display = df_cons.copy()
    if "disponible" in df_cons_display.columns:
        df_cons_display["Disponibilidad"] = df_cons_display["disponible"].map({
            True: "✅ Disponible",
            False: "❌ No disponible",
        }).fillna("❓")

    col_map = {
        "nombre_consultor": "Consultor",
        "especialidad": "Especialidad",
        "Disponibilidad": "Disponibilidad",
        "tipos_aceptados": "Tipos aceptados",
    }
    avail = [k for k in col_map if k in df_cons_display.columns]
    st.dataframe(
        df_cons_display[avail].rename(columns=col_map),
        use_container_width=True,
        hide_index=True,
    )

    # Resumen de disponibilidad
    total = len(df_cons)
    disponibles = int(df_cons["disponible"].sum()) if "disponible" in df_cons.columns else 0
    st.caption(f"**{disponibles} de {total}** consultores disponibles actualmente.")
else:
    st.info("Sin datos de consultores disponibles.")

# ------------------------------------------------------------------
# Info del sistema
# ------------------------------------------------------------------
st.markdown('<p class="section-title">ℹ️ Información del Sistema</p>', unsafe_allow_html=True)

active_url     = st.session_state.get("n8n_url_override", _url)
active_key     = st.session_state.get("n8n_key_override", _key)
active_webhook = st.session_state.get("n8n_webhook_override", _webhook)

col_i1, col_i2 = st.columns(2)
with col_i1:
    st.markdown(f"**N8N URL configurada:** `{active_url}`")
    st.markdown(f"**API Key:** `{'***' + active_key[-4:] if active_key else 'No configurada'}`")
    st.markdown(f"**Webhook URL:** `{active_webhook}`")
with col_i2:
    try:
        _ = st.secrets["n8n"]
        secrets_source = "✅ st.secrets (Streamlit Cloud)"
    except (KeyError, FileNotFoundError):
        secrets_source = "⚠ .env / variables de entorno (local)"
    st.markdown(f"**Fuente de credenciales:** {secrets_source}")
    st.markdown(f"**Sesión overrides activos:** {'✅ Sí' if 'n8n_url_override' in st.session_state else 'No'}")

st.divider()
st.info(
    "💡 **Modo de datos:** Si n8n no está disponible, el dashboard usa datos mock "
    "realistas para desarrollo. Todos los gráficos y análisis funcionan en modo mock."
)

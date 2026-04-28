"""
Cliente de acceso a datos de n8n con estrategia de fallback en tres niveles:
  1. API directa de DataTable de n8n (usando tableId, no tableName)
  2. Webhook de n8n configurado para exportar datos
  3. Datos mock para desarrollo
"""
import os
import json
import requests
import pandas as pd
import streamlit as st
from typing import Optional
from dotenv import load_dotenv
from utils.mock_data import MOCK_TABLES

REQUEST_TIMEOUT = 10

# Mapa estático de nombre → ID real de cada tabla en n8n.
# Obtenido via GET /api/v1/data-tables (listTables).
TABLE_ID_MAP = {
    "experiment_log":          "wbKJYSofIL4iogO6",
    "evaluation_results":      "AqragtdU3W5jqfgB",
    "ground_truth":            "hLlP1T2bhtnU1dgf",
    "dataset_snapshots":       "9V47ca4KgfWF5OeA",
    "linkedin_jobs":           "C8e9dx9Iy4JCCCZH",
    "linkedin_posts":          "WZdnrDRYDsagkd5F",
    "resultados_match":        "2Qz3asU5786l8ZXe",
    "Consultores":             "NdmwL0uqhJpjHCD6",
    "pipeline_runs":           "Qic9jms0v7lpNcpB",
    "pipeline_discard_metrics":"6rxXDLti8AMcRtSM",
    "linkedin_media":          "DVTAz1iIdQHo83OV",
    "linkedin_ocr_results":    "lRKIKRV1YN2FMqF9",
}


def _load_credentials():
    """
    Carga credenciales con prioridad:
    1. st.secrets["n8n"] → Streamlit Cloud / producción
    2. os.getenv / .env  → desarrollo local
    3. Valores por defecto → activa modo mock automáticamente
    """
    try:
        secrets = st.secrets["n8n"]
        return (
            secrets.get("url", "http://localhost:5678"),
            secrets.get("api_key", ""),
            secrets.get("webhook", "http://localhost:5678/webhook"),
        )
    except (KeyError, FileNotFoundError):
        load_dotenv()
        return (
            os.getenv("N8N_URL", "http://localhost:5678"),
            os.getenv("N8N_API_KEY", ""),
            os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook"),
        )


@st.cache_data(ttl=300, show_spinner=False)
def _cached_fetch(base_url: str, api_key: str, webhook_base: str, table_name: str) -> pd.DataFrame:
    """Cache keyed en credenciales + nombre de tabla.
    Al cambiar credenciales, la key cambia y no se devuelve mock cacheado."""
    client = N8NClient(base_url=base_url, api_key=api_key, webhook_base=webhook_base)
    df = client._fetch_via_direct_api(table_name)
    if df is not None:
        return df
    df = client._fetch_via_webhook(table_name)
    if df is not None:
        return df
    return client._fetch_mock(table_name)


class N8NClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 webhook_base: Optional[str] = None):
        _url, _key, _webhook = _load_credentials()
        self.base_url = (base_url or _url).rstrip("/")
        self.api_key = api_key or _key
        self.webhook_base = webhook_base or _webhook
        self._headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
        }

    # ------------------------------------------------------------------
    # Método principal: usa cache standalone (credenciales en la key)
    # ------------------------------------------------------------------

    def get_table(self, table_name: str) -> pd.DataFrame:
        return _cached_fetch(self.base_url, self.api_key, self.webhook_base, table_name)

    def get_table_no_cache(self, table_name: str) -> pd.DataFrame:
        df = self._fetch_via_direct_api(table_name)
        if df is not None:
            return df
        df = self._fetch_via_webhook(table_name)
        if df is not None:
            return df
        return self._fetch_mock(table_name)

    # ------------------------------------------------------------------
    # Nivel 1: API directa — resuelve nombre → tableId
    # ------------------------------------------------------------------

    def _get_table_id(self, table_name: str) -> Optional[str]:
        """Devuelve el ID de la tabla. Primero busca en el mapa estático,
        luego consulta la API si no está registrada."""
        if table_name in TABLE_ID_MAP:
            return TABLE_ID_MAP[table_name]
        # Intento dinámico: listar tablas y buscar por nombre
        try:
            url = f"{self.base_url}/api/v1/data-tables"
            resp = requests.get(url, headers=self._headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                body = resp.json()
                # data puede ser lista directa o dict con clave "tables"
                data = body.get("data", [])
                tables = data if isinstance(data, list) else data.get("tables", [])
                for t in tables:
                    if t.get("name") == table_name:
                        return t.get("id")
        except Exception:
            pass
        return None

    def _fetch_via_direct_api(self, table_name: str) -> Optional[pd.DataFrame]:
        if not self.api_key:
            return None
        table_id = self._get_table_id(table_name)
        if not table_id:
            return None
        try:
            all_rows = []
            cursor = None
            while True:
                url = f"{self.base_url}/api/v1/data-tables/{table_id}/rows"
                params = {"limit": 100}
                if cursor:
                    params["cursor"] = cursor
                resp = requests.get(url, headers=self._headers, params=params, timeout=REQUEST_TIMEOUT)
                if resp.status_code != 200:
                    return None
                body = resp.json()

                # n8n puede devolver filas en distintos formatos — manejamos todos
                if isinstance(body, list):
                    rows = body
                    next_cursor = None
                elif "data" in body and isinstance(body["data"], dict):
                    rows = body["data"].get("rows", [])
                    next_cursor = body["data"].get("nextCursor")
                elif "data" in body and isinstance(body["data"], list):
                    rows = body["data"]
                    next_cursor = body.get("nextCursor")
                elif "rows" in body:
                    rows = body["rows"]
                    next_cursor = body.get("nextCursor")
                else:
                    rows = []
                    next_cursor = None

                all_rows.extend(rows)
                cursor = next_cursor
                if not cursor:
                    break

            if all_rows:
                # Las filas vienen planas: {col1: val, col2: val, ..., id: N, createdAt, updatedAt}
                # No hay campo "data" anidado — tomamos la fila tal cual
                return pd.DataFrame(all_rows)
            return None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Nivel 2: Webhook de exportación
    # ------------------------------------------------------------------

    def _fetch_via_webhook(self, table_name: str) -> Optional[pd.DataFrame]:
        if not self.webhook_base:
            return None
        try:
            url = f"{self.webhook_base}/get-table-data"
            payload = {"table": table_name}
            resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                rows = data.get("rows", data.get("data", data))
                if isinstance(rows, list) and len(rows) > 0:
                    return pd.DataFrame(rows)
            return None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Nivel 3: Mock
    # ------------------------------------------------------------------

    def _fetch_mock(self, table_name: str) -> pd.DataFrame:
        fn = MOCK_TABLES.get(table_name)
        if fn:
            return fn()
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Inserción de fila (para Ground Truth)
    # ------------------------------------------------------------------

    def insert_row(self, table_name: str, data: dict) -> bool:
        table_id = self._get_table_id(table_name)
        if self.api_key and table_id:
            try:
                url = f"{self.base_url}/api/v1/data-tables/{table_id}/rows"
                resp = requests.post(url, json={"data": [data]}, headers=self._headers, timeout=REQUEST_TIMEOUT)
                if resp.status_code in (200, 201):
                    return True
            except Exception:
                pass
        # Fallback: webhook
        try:
            url = f"{self.webhook_base}/insert-row"
            resp = requests.post(url, json={"table": table_name, "data": data}, timeout=REQUEST_TIMEOUT)
            return resp.status_code in (200, 201)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Diagnóstico de conexión
    # ------------------------------------------------------------------

    def test_connection(self) -> dict:
        results = {
            "api_reachable": False,
            "api_key_valid": False,
            "webhook_reachable": False,
            "tables": {},
        }
        # Probar API base
        try:
            url = f"{self.base_url}/api/v1/data-tables"
            resp = requests.get(url, headers=self._headers, timeout=REQUEST_TIMEOUT)
            results["api_reachable"] = True
            results["api_key_valid"] = resp.status_code == 200
        except Exception as e:
            results["api_error"] = str(e)

        # Probar webhook
        try:
            url = f"{self.webhook_base}/get-table-data"
            resp = requests.post(url, json={"table": "ping"}, timeout=5)
            results["webhook_reachable"] = resp.status_code in (200, 404)
        except Exception:
            pass

        # Estado de cada tabla
        for table in list(TABLE_ID_MAP.keys()) + [t for t in MOCK_TABLES if t not in TABLE_ID_MAP]:
            df_direct = self._fetch_via_direct_api(table)
            df_webhook = self._fetch_via_webhook(table) if df_direct is None else None

            source = "api_directa" if df_direct is not None else ("webhook" if df_webhook is not None else "mock")
            df = df_direct if df_direct is not None else (df_webhook if df_webhook is not None else self._fetch_mock(table))
            results["tables"][table] = {
                "source": source,
                "rows": len(df) if df is not None else 0,
                "ok": source != "mock",
            }

        return results


def get_client() -> N8NClient:
    _url, _key, _webhook = _load_credentials()
    if "n8n_client" not in st.session_state:
        st.session_state.n8n_client = N8NClient(base_url=_url, api_key=_key, webhook_base=_webhook)
    return st.session_state.n8n_client


def safe_json_parse(value, default=None):
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default

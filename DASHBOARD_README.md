# Latinnova — Dashboard de Pipeline de IA

Dashboard interactivo en Streamlit para visualizar los resultados del pipeline de matching
consultor-oportunidad desarrollado en n8n para el proyecto de maestría Latinnova.

---

## Instalación

### 1. Clonar / descargar el proyecto

```bash
cd latinnova_dashboard
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores reales:

```
N8N_URL=http://localhost:5678        # URL de tu instancia n8n
N8N_API_KEY=tu_api_key_aqui          # Settings → API Keys en n8n
WEBHOOK_URL=http://localhost:5678/webhook
```

> Si no configuras el `.env`, el dashboard arranca en **modo demo** con datos mock realistas.

---

## Ejecución

```bash
streamlit run dashboard.py
```

El dashboard abre automáticamente en `http://localhost:8501`.

---

## Estructura del proyecto

```
latinnova_dashboard/
├── dashboard.py              # Página principal (KPIs, métricas, pipeline runs)
├── requirements.txt
├── .env.example
├── DASHBOARD_README.md
├── utils/
│   ├── __init__.py
│   ├── n8n_client.py         # Cliente API n8n con fallback a webhook y mock
│   └── mock_data.py          # Datos de prueba realistas basados en experimentos reales
└── pages/
    ├── 1_Matches.py          # Resultados de matching con filtros
    ├── 2_Experimentos.py     # Análisis comparativo de experimentos
    ├── 3_Oportunidades.py    # Explorador de oportunidades clasificadas
    ├── 4_Ground_Truth.py     # Validación humana y formulario de evaluación
    └── 5_Configuracion.py    # Configuración de conexión a n8n
```

---

## Descripción de páginas

| Página | Descripción |
|---|---|
| **Dashboard** | KPIs globales, evolución Precision/Recall/F1, pipeline runs recientes |
| **Matches** | Tabla de matches con filtros por tipo/consultor/score, Top 10, distribución por tipo |
| **Experimentos** | Comparativa de exp_001-004, radar chart, matriz de confusión, análisis GPT |
| **Oportunidades** | Explorador de LinkedIn jobs con filtros avanzados y tarjetas de detalle |
| **Ground Truth** | Tabla de evaluaciones humanas, accuracy vs F1, formulario de nuevas evaluaciones |
| **Configuración** | Conexión a n8n, prueba de tablas, gestión de consultores |

---

## Estrategia de acceso a datos

El cliente `N8NClient` implementa fallback automático en 3 niveles:

```
1. API directa de n8n DataTable
   GET /api/v1/data-tables/{tableName}/rows
   Headers: { "X-N8N-API-KEY": "<api_key>" }
        ↓ (si falla)
2. Webhook de exportación
   POST /webhook/get-table-data
   Body: { "table": "nombre_tabla" }
        ↓ (si falla)
3. Datos mock (utils/mock_data.py)
   DataFrames con datos realistas para desarrollo
```

---

## Configurar el Webhook en n8n (Fallback)

Para habilitar el fallback por webhook, crear un workflow en n8n:

### Pasos:

1. Abrir n8n → New Workflow
2. Agregar nodo **Webhook**:
   - HTTP Method: `POST`
   - Path: `get-table-data`
   - Response Mode: `Last Node`

3. Agregar nodo **Switch** conectado al Webhook:
   - Modo: Rules
   - Field: `{{ $json.body.table }}`
   - Agregar un caso por cada tabla (linkedin_jobs, Consultores, etc.)

4. Por cada caso, agregar un nodo **n8n DataTable** (Read):
   - Table: nombre de la tabla correspondiente

5. Conectar todos los casos a un nodo **Respond to Webhook**:
   - Response Body: `{{ $json }}`

6. Activar el workflow.

Una vez activo, el dashboard detecta automáticamente el webhook y lo usa como fallback.

---

## Tablas del sistema

| Tabla | Descripción |
|---|---|
| `linkedin_posts` | Posts de LinkedIn scrapeados |
| `linkedin_jobs` | Oportunidades clasificadas por tipo |
| `Consultores` | Registro de consultores y disponibilidad |
| `resultados_match` | Resultados del pipeline de matching |
| `experiment_log` | Log de experimentos con métricas |
| `evaluation_results` | Evaluación detallada con análisis IA |
| `ground_truth` | Evaluaciones humanas de pares |
| `dataset_snapshots` | Snapshots del dataset por experimento |
| `pipeline_runs` | Historial de ejecuciones del pipeline |

---

## 🔄 Actualizar URL de ngrok

Cuando reinicies ngrok, la URL pública cambiará. Para reconectar el dashboard:

1. Obtén la nueva URL de ngrok (ej: `https://nueva-url.ngrok-free.app`)
2. Ve a Streamlit Cloud → tu app → **⋮ → Settings → Secrets**
3. Actualiza los valores:
   ```toml
   [n8n]
   url     = "https://nueva-url.ngrok-free.app"
   api_key = "tu_api_key"   # esta no cambia
   webhook = "https://nueva-url.ngrok-free.app/webhook"
   ```
4. Clic en **Save** → la app se reiniciará automáticamente con la nueva URL

**Alternativa:** Para evitar este proceso, considera usar ngrok con un dominio fijo
(plan de pago) o migrar n8n a un servicio cloud como Railway o Render.

---

## Notas de desarrollo

- El caché de datos tiene un TTL de 300 segundos (5 minutos)
- Usar el botón "🔄 Refrescar datos" para forzar recarga desde n8n
- Los campos JSON serializados (`todos_los_resultados`, `tipos_aceptados`, etc.) 
  son parseados automáticamente por `safe_json_parse()` con manejo de excepciones
- El modo mock activa automáticamente si `N8N_API_KEY` no está configurada

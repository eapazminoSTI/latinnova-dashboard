"""
Datos mock realistas para desarrollo sin conexión a n8n.
Basados en los experimentos reales del proyecto Latinnova.
"""
import pandas as pd
import json
from datetime import datetime, timedelta


def get_linkedin_posts() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "post_id": "post_001",
            "post_text": "Se abre convocatoria para consultoría en transformación digital para PYMEs de la región andina. Requisitos: experiencia mínima 5 años en gestión de cambio organizacional.",
            "author_name": "BID Lab",
            "post_date": "2024-03-01",
            "url": "https://linkedin.com/posts/bidlab_001"
        },
        {
            "post_id": "post_002",
            "post_text": "Financiamiento disponible para startups de impacto social en Latinoamérica. Hasta USD 50.000 en capital semilla. Postulaciones hasta el 30 de abril.",
            "author_name": "Latimpacto",
            "post_date": "2024-03-05",
            "url": "https://linkedin.com/posts/latimpacto_002"
        },
        {
            "post_id": "post_003",
            "post_text": "Evento: Cumbre de Innovación Social 2024 en Bogotá. Panelistas de todo el continente discutirán el futuro de las economías emergentes.",
            "author_name": "SEKN",
            "post_date": "2024-03-10",
            "url": "https://linkedin.com/posts/sekn_003"
        },
    ])


def get_linkedin_jobs() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "post_id": "job_001",
            "cargo": "Consultor en Transformación Digital",
            "ciudad": "Bogotá",
            "pais": "Colombia",
            "objetivo_del_cargo": "Acompañar a PYMEs en su proceso de digitalización con énfasis en automatización de procesos y cultura organizacional.",
            "prerrequisitos": "5+ años en consultoría, experiencia con metodologías ágiles, inglés B2+",
            "aplica_en": "https://bidlab.org/convocatoria-digital",
            "fecha_limite": "2024-04-30",
            "tipo_oportunidad": "consultoría",
            "confianza_clasificacion": 0.92,
            "razon_clasificacion": "El cargo describe claramente un rol de consultoría con objetivos definidos y no implica relación de dependencia laboral.",
            "URL": "https://picsum.photos/seed/job001/800/600",
        },
        {
            "post_id": "job_002",
            "cargo": "Director de Innovación",
            "ciudad": "Lima",
            "pais": "Perú",
            "objetivo_del_cargo": "Liderar estrategia de innovación en organización de desarrollo social con presencia regional.",
            "prerrequisitos": "MBA o equivalente, 8+ años en sector social, red de contactos en ecosistema de innovación",
            "aplica_en": "https://empresa.pe/vacante-001",
            "fecha_limite": "2024-05-15",
            "tipo_oportunidad": "empleo",
            "confianza_clasificacion": 0.88,
            "razon_clasificacion": "Perfil de empleo de tiempo completo con dependencia organizacional clara.",
            "URL": "https://picsum.photos/seed/job002/800/600",
        },
        {
            "post_id": "job_003",
            "cargo": "Fondo Semilla — Startups de Impacto",
            "ciudad": "Ciudad de México",
            "pais": "México",
            "objetivo_del_cargo": "Financiamiento no reembolsable para startups en etapa temprana con modelo de negocio de impacto social medible.",
            "prerrequisitos": "Empresa constituida, equipo de al menos 2 personas, prototipo validado",
            "aplica_en": "https://latimpacto.org/fondo-semilla",
            "fecha_limite": "2024-04-30",
            "tipo_oportunidad": "financiamiento",
            "confianza_clasificacion": 0.95,
            "razon_clasificacion": "Convocatoria de financiamiento con capital no reembolsable, no es empleo ni consultoría.",
            "URL": "https://picsum.photos/seed/job003/800/600",
        },
        {
            "post_id": "job_004",
            "cargo": "Programa de Formación en Liderazgo Social",
            "ciudad": "Santiago",
            "pais": "Chile",
            "objetivo_del_cargo": "Programa de 6 meses para fortalecer capacidades de liderazgo en líderes de organizaciones sociales de la región.",
            "prerrequisitos": "Líderes con al menos 3 años de experiencia en sector social, postulación con carta de motivación",
            "aplica_en": "https://ashoka.org/fellows-programa",
            "fecha_limite": "2024-06-01",
            "tipo_oportunidad": "formación",
            "confianza_clasificacion": 0.90,
            "razon_clasificacion": "Programa educativo con componente práctico, no genera remuneración sino capacitación.",
            "URL": "https://picsum.photos/seed/job004/800/600",
        },
        {
            "post_id": "job_005",
            "cargo": "Cumbre de Innovación Social 2024",
            "ciudad": "Bogotá",
            "pais": "Colombia",
            "objetivo_del_cargo": "Conferencia anual para líderes de innovación social, con talleres, paneles y oportunidades de networking.",
            "prerrequisitos": "Registro previo requerido, cupos limitados",
            "aplica_en": "https://sekn.org/cumbre-2024",
            "fecha_limite": "2024-05-01",
            "tipo_oportunidad": "evento",
            "confianza_clasificacion": 0.97,
            "razon_clasificacion": "Evento presencial de networking y conocimiento, sin remuneración ni vínculo laboral.",
            "URL": "https://picsum.photos/seed/job005/800/600",
        },
        {
            "post_id": "job_006",
            "cargo": "Investigador Asociado — Economías Emergentes",
            "ciudad": "Buenos Aires",
            "pais": "Argentina",
            "objetivo_del_cargo": "Investigación aplicada sobre modelos de negocio inclusivos en mercados de base de la pirámide.",
            "prerrequisitos": "Doctorado en economía, ciencias sociales o campo relacionado, publicaciones indexadas",
            "aplica_en": "https://universidad.edu.ar/investigacion",
            "fecha_limite": "2024-05-20",
            "tipo_oportunidad": "empleo",
            "confianza_clasificacion": 0.85,
            "razon_clasificacion": "Posición académica con vínculo de dependencia institucional.",
            "URL": "https://picsum.photos/seed/job006/800/600",
        },
        {
            "post_id": "job_007",
            "cargo": "Consultoría en Evaluación de Impacto",
            "ciudad": "Quito",
            "pais": "Ecuador",
            "objetivo_del_cargo": "Evaluar impacto social de programa de microfinanzas en zonas rurales del Ecuador usando metodologías cuantitativas.",
            "prerrequisitos": "Experiencia en evaluación de impacto, conocimiento de métodos mixtos, disponibilidad para trabajo en campo",
            "aplica_en": "https://bid.int/consultoría-ecuador",
            "fecha_limite": "2024-04-25",
            "tipo_oportunidad": "consultoría",
            "confianza_clasificacion": 0.93,
            "razon_clasificacion": "Consultoría específica con entregables definidos y período acotado."
        },
        {
            "post_id": "job_008",
            "cargo": "Grant — Investigación en IA para el Bien Social",
            "ciudad": "Montevideo",
            "pais": "Uruguay",
            "objetivo_del_cargo": "Fondo de investigación para proyectos que usen inteligencia artificial para resolver problemas sociales en Latinoamérica.",
            "prerrequisitos": "Institución académica o sin fines de lucro, propuesta de investigación de 18 meses máximo",
            "aplica_en": "https://omidyar.network/grant-ia",
            "fecha_limite": "2024-07-01",
            "tipo_oportunidad": "financiamiento",
            "confianza_clasificacion": 0.89,
            "razon_clasificacion": "Grant de investigación, financiamiento no reembolsable con propósito investigativo."
        },
    ])


def get_consultores() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "nombre_consultor": "Ricardo González",
            "especialidad": "Transformación Digital y Automatización",
            "disponible": True,
            "tipos_aceptados": json.dumps(["consultoría", "formación", "evento"])
        },
        {
            "nombre_consultor": "Andrés Cueva",
            "especialidad": "Innovación Social y Emprendimiento",
            "disponible": True,
            "tipos_aceptados": json.dumps(["consultoría", "financiamiento", "empleo"])
        },
        {
            "nombre_consultor": "María Fernanda Vásquez",
            "especialidad": "Evaluación de Impacto y Metodologías Mixtas",
            "disponible": False,
            "tipos_aceptados": json.dumps(["consultoría", "financiamiento"])
        },
        {
            "nombre_consultor": "Carlos Mendoza",
            "especialidad": "Finanzas Sociales y Microfinanzas",
            "disponible": True,
            "tipos_aceptados": json.dumps(["financiamiento", "consultoría", "empleo"])
        },
        {
            "nombre_consultor": "Laura Jiménez",
            "especialidad": "Liderazgo Organizacional y Cultura",
            "disponible": True,
            "tipos_aceptados": json.dumps(["empleo", "formación", "evento"])
        },
    ])


def get_resultados_match() -> pd.DataFrame:
    top_10 = [
        {"rank": 1, "score_match": 0.77, "nombre_consultor": "Ricardo González", "nombre_oportunidad": "Consultor en Transformación Digital", "tipo_oportunidad": "consultoría", "motivo": "Alta alineación entre especialidad en transformación digital del consultor y el perfil requerido. El consultor tiene experiencia documentada en automatización y agilidad.", "decision": "aplicar", "consultor_id": "c_001", "oportunidad_id": "job_001"},
        {"rank": 2, "score_match": 0.76, "nombre_consultor": "Andrés Cueva", "nombre_oportunidad": "Fondo Semilla — Startups de Impacto", "tipo_oportunidad": "financiamiento", "motivo": "El consultor tiene experiencia en emprendimiento de impacto y ha trabajado con startups en etapa temprana. El fondo es coherente con su perfil.", "decision": "aplicar", "consultor_id": "c_002", "oportunidad_id": "job_003"},
        {"rank": 3, "score_match": 0.75, "nombre_consultor": "Ricardo González", "nombre_oportunidad": "Consultoría en Evaluación de Impacto", "tipo_oportunidad": "consultoría", "motivo": "Aunque la especialidad principal es digital, el consultor tiene habilidades complementarias en análisis cuantitativo relevantes para evaluación.", "decision": "aplicar", "consultor_id": "c_001", "oportunidad_id": "job_007"},
        {"rank": 4, "score_match": 0.74, "nombre_consultor": "Carlos Mendoza", "nombre_oportunidad": "Consultoría en Evaluación de Impacto", "tipo_oportunidad": "consultoría", "motivo": "Perfil financiero con experiencia en microfinanzas es altamente relevante para evaluación de programas similares.", "decision": "aplicar", "consultor_id": "c_004", "oportunidad_id": "job_007"},
        {"rank": 5, "score_match": 0.74, "nombre_consultor": "Laura Jiménez", "nombre_oportunidad": "Programa de Formación en Liderazgo Social", "tipo_oportunidad": "formación", "motivo": "Especialidad en liderazgo organizacional es directamente aplicable al programa de formación de líderes sociales.", "decision": "aplicar", "consultor_id": "c_005", "oportunidad_id": "job_004"},
        {"rank": 6, "score_match": 0.73, "nombre_consultor": "Andrés Cueva", "nombre_oportunidad": "Director de Innovación", "tipo_oportunidad": "empleo", "motivo": "Perfil de innovación social del consultor coincide con el cargo, aunque es empleo de tiempo completo, el consultor indicó aceptar empleo.", "decision": "aplicar", "consultor_id": "c_002", "oportunidad_id": "job_002"},
        {"rank": 7, "score_match": 0.73, "nombre_consultor": "Carlos Mendoza", "nombre_oportunidad": "Grant — Investigación en IA para el Bien Social", "tipo_oportunidad": "financiamiento", "motivo": "Experiencia en finanzas sociales y acceso a redes académicas hace al consultor candidato válido para gestionar este grant.", "decision": "aplicar", "consultor_id": "c_004", "oportunidad_id": "job_008"},
        {"rank": 8, "score_match": 0.72, "nombre_consultor": "Ricardo González", "nombre_oportunidad": "Cumbre de Innovación Social 2024", "tipo_oportunidad": "evento", "motivo": "El evento de networking es relevante para ampliar red de contactos en el ecosistema digital-social donde opera el consultor.", "decision": "aplicar", "consultor_id": "c_001", "oportunidad_id": "job_005"},
        {"rank": 9, "score_match": 0.72, "nombre_consultor": "Laura Jiménez", "nombre_oportunidad": "Cumbre de Innovación Social 2024", "tipo_oportunidad": "evento", "motivo": "Evento alineado con área de liderazgo organizacional y oportunidad de visibilidad profesional.", "decision": "aplicar", "consultor_id": "c_005", "oportunidad_id": "job_005"},
        {"rank": 10, "score_match": 0.72, "nombre_consultor": "Andrés Cueva", "nombre_oportunidad": "Consultor en Transformación Digital", "tipo_oportunidad": "consultoría", "motivo": "Aunque la especialidad principal es innovación social, el consultor tiene competencias digitales secundarias relevantes para el cargo.", "decision": "aplicar", "consultor_id": "c_002", "oportunidad_id": "job_001"},
    ]

    todos_resultados = top_10 + [
        {"rank": 11, "score_match": 0.68, "nombre_consultor": "María Fernanda Vásquez", "nombre_oportunidad": "Consultoría en Evaluación de Impacto", "tipo_oportunidad": "consultoría", "motivo": "Especialidad en evaluación es muy relevante, pero la consultora está marcada como no disponible.", "decision": "no_aplicar", "consultor_id": "c_003", "oportunidad_id": "job_007"},
        {"rank": 12, "score_match": 0.65, "nombre_consultor": "María Fernanda Vásquez", "nombre_oportunidad": "Grant — Investigación en IA", "tipo_oportunidad": "financiamiento", "motivo": "No disponible actualmente según registro del sistema.", "decision": "no_aplicar", "consultor_id": "c_003", "oportunidad_id": "job_008"},
    ]

    dist = json.dumps({
        "consultoría": 4,
        "financiamiento": 3,
        "empleo": 1,
        "evento": 2,
        "formación": 1,
        "otro": 0
    })

    return pd.DataFrame([
        {
            "fecha_ejecucion": "2024-03-15T10:30:00",
            "total_matches_aplicar": 10,
            "distribucion_por_tipo": dist,
            "top_10_matches": json.dumps(top_10),
            "todos_los_resultados": json.dumps(todos_resultados)
        }
    ])


def get_experiment_log() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "experiment_id": "exp_001",
            "prompt_template": "Prompt base sin contexto de especialidad. Comparación directa por palabras clave entre cargo y perfil del consultor.",
            "prompt_hash": "v1.0",
            "precision": 1.0,
            "recall": 0.5,
            "f1": 0.667,
            "total_pares_evaluados": 20,
            "fecha_ejecucion": "2024-03-01T09:00:00"
        },
        {
            "experiment_id": "exp_002",
            "prompt_template": "Prompt con instrucción de ser conservador: solo recomendar si hay certeza absoluta. Umbral de score muy alto (>0.9).",
            "prompt_hash": "v2.0",
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "total_pares_evaluados": 20,
            "fecha_ejecucion": "2024-03-05T14:00:00"
        },
        {
            "experiment_id": "exp_003",
            "prompt_template": "Prompt enriquecido con contexto de 6 tipos de oportunidades y criterios de matching por dominio de especialidad.",
            "prompt_hash": "v3.0",
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
            "total_pares_evaluados": 20,
            "fecha_ejecucion": "2024-03-10T11:00:00"
        },
        {
            "experiment_id": "exp_004",
            "prompt_template": "Mismo prompt v3.0 pero con consultores marcados como disponible=false para probar filtro de disponibilidad.",
            "prompt_hash": "v3.0",
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "total_pares_evaluados": 12,
            "fecha_ejecucion": "2024-03-15T16:00:00"
        },
    ])


def get_evaluation_results() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "experiment_id": "exp_001",
            "tp": 10, "fp": 0, "fn": 10, "tn": 0,
            "precision": 1.0, "recall": 0.5, "f1": 0.667,
            "resumen_ejecutivo": "El experimento 1 logró precisión perfecta pero recall limitado. El modelo solo recomendó casos con alta certeza, perdiendo oportunidades válidas.",
            "fortalezas": "Cero falsos positivos. Todas las recomendaciones emitidas fueron correctas.",
            "debilidades": "Solo identificó el 50% de los matches válidos. El umbral implícito del prompt era demasiado restrictivo.",
            "recomendaciones": "Reducir el umbral de decisión o enriquecer el prompt con más contexto sobre cada tipo de oportunidad.",
            "conclusion_para_tesis": "El experimento 1 establece una línea base de alta precisión. Demuestra que el modelo LLM es capaz de hacer recomendaciones correctas, pero necesita mejor especificación para alcanzar cobertura completa.",
            "analisis_ia": "**Análisis del Experimento 1 — exp_001**\n\n**Contexto:** Se utilizó un prompt base sin contexto especializado de dominio. El modelo GPT-4o recibió únicamente el perfil del consultor y la descripción del cargo sin instrucciones adicionales sobre los criterios de matching.\n\n**Hallazgos principales:**\nEl modelo demostró una capacidad de discriminación notable: cuando decidió recomendar, lo hizo con alta precisión (P=1.0). Sin embargo, su comportamiento conservador — posiblemente derivado del entrenamiento RLHF que penaliza las alucinaciones — lo llevó a abstenerse en casos donde un humano expert sí recomendaría.\n\n**Interpretación del bajo recall:**\nEl recall de 0.5 indica que el modelo 'no vio' el 50% de los matches válidos. Esto no implica que el modelo sea incapaz de identificarlos, sino que el prompt no le proporcionó suficiente contexto para justificar la recomendación con confianza.\n\n**Implicaciones para el diseño del prompt:**\nLa ausencia de instrucciones sobre los 6 tipos de oportunidades obligó al modelo a hacer inferencias propias, generando un sesgo hacia tipos más familiares (consultoría, empleo) y descartando financiamiento y formación.\n\n**Relevancia para la tesis:**\nEste experimento valida la hipótesis de que el prompt engineering es determinante en el rendimiento del sistema. La diferencia entre exp_001 y exp_003 (F1: 0.667 vs 1.0) demuestra empíricamente el valor de la especificación de dominio en sistemas RAG aplicados a matching de talento."
        },
        {
            "experiment_id": "exp_002",
            "tp": 0, "fp": 0, "fn": 20, "tn": 0,
            "precision": 0.0, "recall": 0.0, "f1": 0.0,
            "resumen_ejecutivo": "El experimento 2 fue un caso límite de over-restriction. La instrucción de ser conservador bloqueó completamente las recomendaciones.",
            "fortalezas": "Demostró la sensibilidad del sistema a las instrucciones del prompt. Ningún falso positivo.",
            "debilidades": "Cero recomendaciones emitidas. El sistema fue inutilizable en esta configuración.",
            "recomendaciones": "Nunca usar umbrales de certeza absoluta en sistemas de matching. El dominio admite incertidumbre inherente.",
            "conclusion_para_tesis": "El experimento 2 es un contra-ejemplo valioso: ilustra cómo instrucciones mal calibradas pueden paralizar completamente un sistema de IA, incluso cuando el modelo subyacente tiene la capacidad de hacer el matching.",
            "analisis_ia": "**Análisis del Experimento 2 — exp_002**\n\n**Contexto:** El prompt incluía la instrucción explícita: 'Solo recomienda si tienes certeza absoluta (>90% de confianza). En caso de duda, responde no_aplicar.' Esto creó un umbral inalcanzable en un dominio inherentemente ambiguo.\n\n**Por qué falló totalmente:**\nEl matching de consultores con oportunidades es un problema de juicio experto con incertidumbre intrínseca. Ningún par consultor-oportunidad alcanza 'certeza absoluta' porque:\n1. Los perfiles de consultores son textos cualitativos, no especificaciones técnicas exactas.\n2. Las oportunidades tienen requisitos que se solapan entre múltiples perfiles.\n3. El concepto mismo de 'afinidad' entre perfil y cargo es probabilístico.\n\n**Lección de diseño:**\nEste experimento demuestra que el lenguaje del prompt tiene efectos directos y cuantificables en el comportamiento del sistema. La instrucción 'certeza absoluta' fue interpretada por el modelo como un criterio inalcanzable, generando abstención total.\n\n**Relevancia para la tesis:**\nEste resultado negativo es científicamente valioso porque documenta empíricamente el fenómeno de 'instruction overfit': cuando el prompt sobrespecifica restricciones, el sistema puede colapsar a un estado de no-decisión. Esto tiene implicaciones directas para el diseño de sistemas de IA aplicados en contextos organizacionales reales."
        },
        {
            "experiment_id": "exp_003",
            "tp": 20, "fp": 0, "fn": 0, "tn": 0,
            "precision": 1.0, "recall": 1.0, "f1": 1.0,
            "resumen_ejecutivo": "Experimento 3 alcanzó métricas perfectas. El prompt enriquecido con los 6 tipos de oportunidades y criterios de dominio produjo matching óptimo.",
            "fortalezas": "Precisión y recall perfectos. El sistema identificó correctamente todos los matches válidos sin generar falsos positivos.",
            "debilidades": "Métricas perfectas pueden indicar sobreajuste al conjunto de evaluación actual. Requiere validación con datos externos.",
            "recomendaciones": "Usar este prompt como base de producción. Ampliar el ground truth a más pares para validar la generalización.",
            "conclusion_para_tesis": "El experimento 3 demuestra que un pipeline de IA bien diseñado puede alcanzar métricas óptimas en tareas de matching de talento. El factor diferencial fue la especificación explícita del dominio de conocimiento en el prompt.",
            "analisis_ia": "**Análisis del Experimento 3 — exp_003**\n\n**Contexto:** Prompt v3.0 con especificación completa de los 6 tipos de oportunidades (empleo, consultoría, financiamiento, evento, formación, otro), criterios de matching por dominio y ejemplos de razonamiento esperado.\n\n**Por qué funcionó:**\nEl prompt v3.0 resolvió los problemas identificados en exp_001 y exp_002 mediante:\n1. **Taxonomía explícita:** Definir los 6 tipos eliminó la ambigüedad sobre qué constituye una 'oportunidad relevante'.\n2. **Criterios por dominio:** Especificar qué atributos del perfil son relevantes para cada tipo de oportunidad guió el razonamiento del modelo.\n3. **Balance entre precisión y cobertura:** Eliminar la restricción de 'certeza absoluta' permitió al modelo operar en su zona de competencia.\n\n**Análisis de los errores (TP=20, FP=0, FN=0):**\nLa ausencia total de errores en un conjunto de 20 pares evaluados sugiere que:\n- El conjunto de evaluación es representativo de los casos de uso reales.\n- El prompt captura adecuadamente la lógica de matching del dominio.\n- El modelo GPT-4o tiene capacidad suficiente para este nivel de complejidad.\n\n**Consideraciones de validez:**\nUn F1=1.0 en 20 pares debe interpretarse con cautela. El ground truth fue construido por evaluadores humanos del proyecto, lo que implica cierta subjetividad. La validación real requiere un conjunto de prueba independiente y mayor volumen.\n\n**Relevancia para la tesis:**\nEste resultado confirma la hipótesis central: el prompt engineering puede ser el factor determinante en el rendimiento de sistemas de IA para matching organizacional. El contraste exp_001/exp_002/exp_003 constituye un experimento natural de ablation study que tiene alto valor pedagógico y científico."
        },
        {
            "experiment_id": "exp_004",
            "tp": 0, "fp": 0, "fn": 12, "tn": 0,
            "precision": 0.0, "recall": 0.0, "f1": 0.0,
            "resumen_ejecutivo": "Experimento 4 validó el filtro de disponibilidad. Con todos los consultores marcados como no disponibles, el sistema correctamente no generó recomendaciones.",
            "fortalezas": "El sistema respeta correctamente el campo disponible=false. Comportamiento esperado y correcto.",
            "debilidades": "Al no haber recomendaciones, las métricas colapsan a cero. Esto es un comportamiento correcto, no un fallo del modelo.",
            "recomendaciones": "Documentar este experimento como validación del filtro de disponibilidad. Incluir en la tesis como prueba de robustez del sistema.",
            "conclusion_para_tesis": "El experimento 4 no representa un fallo del sistema sino una validación exitosa del filtro de disponibilidad. Las métricas en cero reflejan el comportamiento correcto: no recomendar consultores no disponibles, independientemente de la calidad del match.",
            "analisis_ia": "**Análisis del Experimento 4 — exp_004**\n\n**Contexto:** Se ejecutó el mismo prompt v3.0 del experimento exitoso (exp_003), pero con todos los consultores marcados como disponible=false en la tabla Consultores de n8n DataTable.\n\n**Interpretación de las métricas en cero:**\nEste experimento requiere una lectura diferente a los anteriores. F1=0.0 no indica que el sistema falló — indica que el sistema funcionó correctamente según las reglas de negocio definidas:\n- Regla: Si un consultor no está disponible, no se genera ninguna recomendación para ese consultor.\n- Resultado: 0 recomendaciones generadas para 12 pares evaluados.\n- Evaluación: Todos los 12 pares fueron marcados como FN porque el ground truth sí los marcaba como matches válidos (basado en afinidad de perfil), pero el sistema los excluyó por disponibilidad.\n\n**Por qué este resultado es valioso:**\nDemostrar que el sistema respeta las restricciones operacionales (disponibilidad) es crucial para la confiabilidad del pipeline en producción. Un sistema que ignore el campo disponible generaría recomendaciones inútiles o dañinas.\n\n**Distinción conceptual para la tesis:**\nEs importante distinguir entre 'incapacidad del modelo' y 'restricción operacional del sistema'. El experimento 4 es del segundo tipo: el modelo es capaz de hacer el matching, pero el sistema filtra correctamente antes de llegar al modelo.\n\n**Relevancia para la tesis:**\nEste experimento añade una dimensión de robustez al análisis: el pipeline no solo debe ser preciso, debe ser operacionalmente correcto. La validación de restricciones de negocio es parte integral de la evaluación de sistemas de IA aplicados."
        },
    ])


def get_ground_truth() -> pd.DataFrame:
    return pd.DataFrame([
        {"par_id": "gt_001", "experiment_id": "exp_003", "oportunidad_id": "job_001", "consultor_id": "c_001", "nombre_oportunidad": "Consultor en Transformación Digital", "nombre_consultor": "Ricardo González", "es_correcto": True, "evaluador": "evaluador_humano_1", "comentario": "Alta alineación confirmada por experto del dominio.", "evaluated_at": "2024-03-11T10:00:00"},
        {"par_id": "gt_002", "experiment_id": "exp_003", "oportunidad_id": "job_003", "consultor_id": "c_002", "nombre_oportunidad": "Fondo Semilla — Startups de Impacto", "nombre_consultor": "Andrés Cueva", "es_correcto": True, "evaluador": "evaluador_humano_1", "comentario": "El consultor tiene experiencia directa en startups de impacto.", "evaluated_at": "2024-03-11T10:15:00"},
        {"par_id": "gt_003", "experiment_id": "exp_003", "oportunidad_id": "job_004", "consultor_id": "c_005", "nombre_oportunidad": "Programa de Formación en Liderazgo", "nombre_consultor": "Laura Jiménez", "es_correcto": True, "evaluador": "evaluador_humano_2", "comentario": "Especialidad directamente aplicable.", "evaluated_at": "2024-03-11T11:00:00"},
        {"par_id": "gt_004", "experiment_id": "exp_003", "oportunidad_id": "job_007", "consultor_id": "c_004", "nombre_oportunidad": "Consultoría en Evaluación de Impacto", "nombre_consultor": "Carlos Mendoza", "es_correcto": True, "evaluador": "evaluador_humano_2", "comentario": "Experiencia en microfinanzas es relevante para evaluación de programas similares.", "evaluated_at": "2024-03-11T11:30:00"},
        {"par_id": "gt_005", "experiment_id": "exp_001", "oportunidad_id": "job_001", "consultor_id": "c_001", "nombre_oportunidad": "Consultor en Transformación Digital", "nombre_consultor": "Ricardo González", "es_correcto": True, "evaluador": "evaluador_humano_1", "comentario": "Match correcto identificado en exp_001 también.", "evaluated_at": "2024-03-02T09:00:00"},
        {"par_id": "gt_006", "experiment_id": "exp_001", "oportunidad_id": "job_002", "consultor_id": "c_002", "nombre_oportunidad": "Director de Innovación", "nombre_consultor": "Andrés Cueva", "es_correcto": False, "evaluador": "evaluador_humano_1", "comentario": "El consultor no indicó interés en empleo de tiempo completo en este experimento.", "evaluated_at": "2024-03-02T09:30:00"},
    ])


def get_dataset_snapshots() -> pd.DataFrame:
    return pd.DataFrame([
        {"snapshot_id": "snap_001", "experiment_id": "exp_001", "total_jobs": 8, "total_consultores": 5, "total_pares_generados": 20, "prompt_hash": "v1.0", "fecha": "2024-03-01"},
        {"snapshot_id": "snap_002", "experiment_id": "exp_002", "total_jobs": 8, "total_consultores": 5, "total_pares_generados": 20, "prompt_hash": "v2.0", "fecha": "2024-03-05"},
        {"snapshot_id": "snap_003", "experiment_id": "exp_003", "total_jobs": 8, "total_consultores": 5, "total_pares_generados": 20, "prompt_hash": "v3.0", "fecha": "2024-03-10"},
        {"snapshot_id": "snap_004", "experiment_id": "exp_004", "total_jobs": 8, "total_consultores": 3, "total_pares_generados": 12, "prompt_hash": "v3.0", "fecha": "2024-03-15"},
    ])


def get_pipeline_runs() -> pd.DataFrame:
    return pd.DataFrame([
        {"run_id": "run_001", "workflow_name": "Latinnova — Clasificación de Oportunidades", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-01T08:55:00", "finished_at": "2024-03-01T09:03:00"},
        {"run_id": "run_002", "workflow_name": "Latinnova — Matching Consultor-Oportunidad", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-01T09:05:00", "finished_at": "2024-03-01T09:22:00"},
        {"run_id": "run_003", "workflow_name": "Latinnova — Evaluación exp_002", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-05T13:58:00", "finished_at": "2024-03-05T14:10:00"},
        {"run_id": "run_004", "workflow_name": "Latinnova — Matching Consultor-Oportunidad", "status": "error", "model_name": "gpt-4o", "errors_count": 3, "started_at": "2024-03-08T10:00:00", "finished_at": "2024-03-08T10:02:00"},
        {"run_id": "run_005", "workflow_name": "Latinnova — Matching Consultor-Oportunidad", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-10T10:55:00", "finished_at": "2024-03-10T11:15:00"},
        {"run_id": "run_006", "workflow_name": "Latinnova — Evaluación exp_003", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-10T11:20:00", "finished_at": "2024-03-10T11:35:00"},
        {"run_id": "run_007", "workflow_name": "Latinnova — Validación Disponibilidad", "status": "success", "model_name": "gpt-4o", "errors_count": 0, "started_at": "2024-03-15T15:58:00", "finished_at": "2024-03-15T16:12:00"},
    ])


# Mapa de funciones para acceso uniforme
MOCK_TABLES = {
    "linkedin_posts": get_linkedin_posts,
    "linkedin_jobs": get_linkedin_jobs,
    "Consultores": get_consultores,
    "resultados_match": get_resultados_match,
    "experiment_log": get_experiment_log,
    "evaluation_results": get_evaluation_results,
    "ground_truth": get_ground_truth,
    "dataset_snapshots": get_dataset_snapshots,
    "pipeline_runs": get_pipeline_runs,
}

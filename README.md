# CasaGen AI — Generación de imágenes, planos y video desde texto

Esta base inicial implementa un **MVP backend** para una aplicación que transforma una descripción en lenguaje natural en:

1. Conceptos visuales (imágenes de fachada/interiores)
2. Planos preliminares (distribución y áreas)
3. Guion/storyboard para video

> Objetivo: ayudar a personas que quieren construir su casa a visualizar ideas antes de contratar diseño técnico final.

## Enfoque recomendado (MVP)

### Flujo de producto

1. Usuario describe su casa ideal (presupuesto, metros, estilo, número de habitaciones, terreno, etc.)
2. El sistema estructura el texto en un `HouseBrief`.
3. Se generan salidas en paralelo:
   - **Imágenes** conceptuales
   - **Plano preliminar** (JSON estructurado + texto explicativo)
   - **Storyboard/video prompt**
4. Usuario itera con feedback: “más iluminación”, “menos costo”, “agregar patio”.

### Arquitectura técnica sugerida

- **API**: FastAPI
- **Orquestación**: servicio Python con proveedor de IA desacoplado por interfaz
- **Generación de imágenes/video**: integración posterior con modelo multimodal externo
- **Persistencia**: PostgreSQL (futuro) para proyectos y versiones
- **Almacenamiento de archivos**: S3 compatible (futuro)

## ¿Dónde copiar este código?

Tienes 2 opciones:

1. **Usar este mismo repositorio (`/workspace/gpt`)** para pruebas locales.
2. **Copiarlo a tu propio proyecto** en una carpeta nueva, por ejemplo:

```bash
mkdir casagen-ai
cd casagen-ai
# copia aquí las carpetas/archivos: app/, tests/, requirements.txt, pytest.ini, README.md
```

Estructura mínima que debes conservar:

```txt
app/
  __init__.py
  main.py
tests/
  test_api.py
requirements.txt
pytest.ini
```

## Estructura actual

```txt
app/
  main.py          # API + orquestador mock para MVP
requirements.txt
tests/
  test_api.py      # pruebas básicas de endpoint
```

## ¿Cómo usar la app? (paso a paso)

### 1) Crear entorno e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Levantar la API

```bash
uvicorn app.main:app --reload
```

### 3) Probar desde el navegador

- Swagger UI: http://127.0.0.1:8000/docs
- Endpoint de salud: `GET /health`
- Endpoint principal: `POST /generate`

Ejemplo de body para `POST /generate`:

```json
{
  "prompt": "Quiero una casa moderna de 2 pisos, 3 habitaciones, patio con jardín y mucha luz natural"
}
```

### 4) Probar desde terminal (sin navegador)

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Quiero una casa moderna de 2 pisos, 3 habitaciones, patio con jardín y mucha luz natural"}'
```

### 5) Ejecutar tests

```bash
pytest -q
```

## Siguientes pasos

1. Conectar un LLM para parsing robusto del texto a `HouseBrief`.
2. Conectar proveedores reales de imagen/video.
3. Implementar motor de validación de reglas mínimas (habitabilidad, áreas, consistencia).
4. Añadir módulo de estimación de costos por m² y materiales.
5. Crear frontend web (chat + galería + visor de plano).

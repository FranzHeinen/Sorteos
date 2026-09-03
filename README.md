# # AutoSorteo Pro

Sorteo de auto 0KM con registro automático en Google Sheets y pagos via Mercado Pago.

## Herramientas utilizadas

- **Python 3.14** - Lenguaje principal
- **FastAPI** - Framework del backend
- **Uvicorn** - Servidor web
- **gspread + google-auth** - Conexion a Google Sheets
- **Mercado Pago SDK** - Pasarela de pagos
- **pydantic** - Validacion de datos
- **HTML5 + CSS3 + JavaScript** - Frontend
- **Render** - Hosting en la nube
- **Git + GitHub** - Control de versiones

## Estadisticas del proyecto

- Frontend (animaciones, formulario, redirect): 100%
- Backend (API, validacion, registro): 100%
- Google Sheets (registro automatico): 100%
- Mercado Pago (link de pago): 100%
- Despliegue en produccion (Render): 100%
- Seguridad (.gitignore, variables entorno): 100%

## Como funciona

1. El usuario elige un producto (llavero, calco o pack) en la web
2. Completa sus datos en el formulario
3. El sistema lo registra en Google Sheets con numeros de sorteo
4. Redirige automaticamente al link de pago de Mercado Pago
5. El pago se confirma y el participante queda habilitado

## Variables de entorno para Render

- GOOGLE_SHEETS_CREDENTIALS_JSON - Credenciales de Google como JSON
- SPREADSHEET_ID - ID de la planilla (1Ot_7fgO0ODteUAdoEg6hXbH3ZPO8xDl_F1yP1fEbuZU)
- WORKSHEET_NAME - Nombre de la hoja (Participantes)
- MP_ACCESS_TOKEN - Token de Mercado Pago
- PAYMENT_URL - Link de pago (https://mpago.la/1ijAQNk)

## Estructura del proyecto

sorteo_auto/
  frontend/
    index.html
    style.css
    script.js
  backend/
    main.py
    app/
      models.py
      config.py
      sheets_service.py
    requirements.txt
    .env.example
    .env
    credentials.json
  README.md

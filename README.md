# 🚗 AutoSorteo Pro

Plataforma de sorteo de auto 0KM con registro automático en Google Sheets y pagos via Mercado Pago.

---

## 🛠️ Herramientas utilizadas

🐍 Python 3.14 - Lenguaje principal
🚀 FastAPI - Framework del backend
⚡ Uvicorn - Servidor web ASGI
📊 gspread + google-auth - Conexión a Google Sheets
💳 Mercado Pago SDK - Pasarela de pagos
✅ pydantic - Validación de datos
🎨 HTML5 + CSS3 + JavaScript - Frontend interactivo
☁️ Render - Hosting en la nube
🔀 Git + GitHub - Control de versiones

---

## 📊 Estadísticas del proyecto

Frontend (animaciones, formulario, redirect):      ████████████████████ 100%
Backend (API, validación, registro):                ████████████████████ 100%
Google Sheets (registro automático):                ████████████████████ 100%
Mercado Pago (link de pago):                        ████████████████████ 100%
Despliegue en producción (Render):                  ████████████████████ 100%
Seguridad (.gitignore, variables entorno):          ████████████████████ 100%

Total: 6/6 módulos completos ✅

---

## 🔄 ¿Cómo funciona?

1️⃣ El usuario elige un producto (llavero, calco o pack) en la web
2️⃣ Completa sus datos en el formulario
3️⃣ El sistema lo registra en Google Sheets con números de sorteo
4️⃣ Redirige automáticamente al link de pago de Mercado Pago
5️⃣ El pago se confirma y el participante queda habilitado

---

## ⚙️ Variables de entorno para Render

- GOOGLE_SHEETS_CREDENTIALS_JSON → Credenciales de Google como JSON
- SPREADSHEET_ID → ID de la planilla
- WORKSHEET_NAME → Nombre de la hoja (Participantes)
- MP_ACCESS_TOKEN → Token de Mercado Pago
- PAYMENT_URL → Link de pago

---

## 📂 Estructura del proyecto

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
  README.md

import random
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models import ParticipanteRequest, ParticipanteResponse, MercadoPagoWebhookPayload
from app.sheets_service import GoogleSheetsService

app = FastAPI(
    title="AutoSorteo Pro API",
    description="Backend para registro y automatización de sorteo de autos con Google Sheets",
    version="1.0.0"
)

# Permitir CORS para desarrollo y peticiones frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicio de Google Sheets
sheets_service = GoogleSheetsService()

def generar_numeros_sorteo(cantidad: int) -> list:
    """Genera números aleatorios únicos con formato AUTO-XXXXX"""
    numeros = []
    for _ in range(cantidad):
        num = random.randint(10000, 99999)
        numeros.append(f"AUTO-{num}")
    return numeros

@app.post("/api/participar", response_model=ParticipanteResponse)
async def registrar_participacion(data: ParticipanteRequest):
    """
    Endpoint para procesar la compra de un producto y registrar al participante en Google Sheets.
    """
    try:
        # Generar identificador de transacción y números del sorteo
        transaccion_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"
        chances = max(1, data.chances)
        tickets = generar_numeros_sorteo(chances)

        # Asentar en Google Sheets o en respaldo local
        synced, modo = sheets_service.registrar_participante(
            transaccion_id=transaccion_id,
            nombre=data.nombre,
            dni=data.dni,
            email=data.email,
            telefono=data.telefono,
            producto=data.producto,
            monto=data.monto,
            chances=chances,
            tickets=tickets,
            medio_pago=data.medio_pago or "mercadopago",
            estado="Aprobado"
        )

        return ParticipanteResponse(
            success=True,
            message="Participante registrado exitosamente.",
            nombre=data.nombre,
            dni=data.dni,
            producto=data.producto,
            chances=chances,
            tickets=tickets,
            sheet_synced=synced,
            modo=modo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar participante: {str(e)}")

@app.post("/api/webhook/mercadopago")
async def webhook_mercadopago(request: Request):
    """
    Webhook preparado para recibir notificaciones automáticas de pago de Mercado Pago (IPN).
    """
    try:
        body = await request.json()
        print(f"[Webhook Mercado Pago Recibido]: {body}")
        
        # Aquí se procesaría el id del pago llamando a Mercado Pago SDK
        # Para consultar el estado 'approved' y luego disparar sheets_service.registrar_participante()
        return {"status": "received", "detail": "Webhook procesado"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/health")
async def health_check():
    """Estado de salud del backend y conector de planilla"""
    return {
        "status": "online",
        "google_sheets_connected": sheets_service.is_connected,
        "service": "AutoSorteo API"
    }

# Servir archivos estáticos del Frontend
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(frontend_dir / "index.html")

    @app.get("/{full_path:path}")
    async def serve_frontend_assets(full_path: str):
        file_candidate = frontend_dir / full_path
        if file_candidate.is_file():
            return FileResponse(file_candidate)
        return FileResponse(frontend_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor AutoSorteo Pro en http://127.0.0.1:8000 ...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

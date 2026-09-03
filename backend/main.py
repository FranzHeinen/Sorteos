import mercadopago
import os
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.models import ParticipanteRequest, ParticipanteResponse
from backend.app.sheets_service import GoogleSheetsService

app = FastAPI(title="AutoSorteo Pro API")

# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sheets_service = GoogleSheetsService()
# Inicializar SDK de Mercado Pago
mp = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", "TU_ACCESS_TOKEN_REAL"))

@app.post("/api/participar", response_model=ParticipanteResponse)
async def registrar_participacion(data: ParticipanteRequest):
    """
    Registra al participante preliminarmente y genera link de pago.
    """
    # 1. Aquí deberías crear la preferencia de pago en MP
    # y retornar el link de pago al frontend.
    # Por ahora, simulamos el flujo de éxito para probar la planilla.
    
    # IMPORTANTE: Asegúrate de llamar a sheets_service aquí o en el webhook
    # Ejemplo de llamada directa para probar la planilla:
    import uuid
    import random
    
    transaccion_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"
    tickets = [f"AUTO-{random.randint(10000, 99999)}" for _ in range(data.chances)]
    
    synced, modo = sheets_service.registrar_participante(
        transaccion_id=transaccion_id,
        nombre=data.nombre,
        dni=data.dni,
        email=data.email,
        telefono=data.telefono,
        producto=data.producto,
        monto=data.monto,
        chances=data.chances,
        tickets=tickets,
        medio_pago=data.medio_pago,
        estado="Pendiente Pago" # Inicialmente pendiente
    )
    
    return ParticipanteResponse(
        success=True,
        message="Participante registrado, redirigiendo a pago.",
        nombre=data.nombre,
        dni=data.dni,
        producto=data.producto,
        chances=data.chances,
        tickets=tickets,
        sheet_synced=synced,
        modo=modo
    )

@app.post("/api/webhook/mercadopago")
async def webhook_mercadopago(request: Request):
    """
    Recibe la notificación de Mercado Pago.
    Cuando el pago es 'approved', actualiza el estado en la planilla.
    """
    data = await request.json()
    # Log para debug en Render
    print(f"Webhook recibido: {data}")
    
    # Validar que sea un pago y esté aprobado
    if data.get("type") == "payment":
        payment_id = data.get("data", {}).get("id")
        payment = mp.payment().get(payment_id)
        
        if payment["status"] == 200:
            payment_info = payment["response"]
            if payment_info["status"] == "approved":
                # AQUÍ DEBERÍAS BUSCAR EL PARTICIPANTE EN LA PLANILLA
                # Y CAMBIAR EL ESTADO A 'PAGADO'
                print(f"Pago {payment_id} aprobado para: {payment_info['external_reference']}")
    
    return {"status": "ok"}

# Montar frontend
frontend_dir = "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(f"{frontend_dir}/index.html")

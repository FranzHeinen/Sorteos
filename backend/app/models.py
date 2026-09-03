from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ParticipanteRequest(BaseModel):
    nombre: str
    email: str
    telefono: str
    dni: str
    producto: str
    monto: float
    chances: int
    medio_pago: Optional[str] = "mercadopago"

class ParticipanteResponse(BaseModel):
    success: bool
    message: str
    nombre: str
    dni: str
    producto: str
    chances: int
    tickets: List[str]
    sheet_synced: bool
    modo: str
    payment_url: Optional[str] = None

class MercadoPagoWebhookPayload(BaseModel):
    action: Optional[str] = None
    type: Optional[str] = None
    data: Optional[dict] = None

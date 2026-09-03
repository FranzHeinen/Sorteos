import os
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

from app.config import (
    CREDENTIALS_FILE,
    SPREADSHEET_NAME,
    WORKSHEET_NAME,
    BACKUP_CSV_FILE,
)

logger = logging.getLogger("sheets_service")

# Encabezados estándar de la planilla
SHEET_HEADERS = [
    "Fecha",
    "Hora",
    "ID Transacción",
    "Nombre y Apellido",
    "DNI",
    "Email",
    "Teléfono",
    "Producto",
    "Monto ($)",
    "Chances",
    "Números de Sorteo",
    "Medio de Pago",
    "Estado"
]

class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self._init_connection()

    def _init_connection(self):
        """Intenta inicializar la conexión con Google Sheets si existe el archivo de credenciales"""
        cred_path = Path(__file__).resolve().parent.parent / CREDENTIALS_FILE
        
        if not cred_path.exists():
            logger.warning(
                f"No se encontró el archivo de credenciales de Google Sheets en '{cred_path}'. "
                "Operando en modo SIMULACIÓN con respaldo en CSV local."
            )
            self.is_connected = False
            return

        try:
            import gspread
            from google.oauth2.service_account import Credentials

            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(str(cred_path), scopes=scopes)
            self.client = gspread.authorize(creds)
            self.is_connected = True
            logger.info("Conexión con Google Sheets establecida exitosamente.")
        except Exception as e:
            logger.error(f"Error al conectar con Google Sheets: {e}")
            self.is_connected = False

    def registrar_participante(
        self,
        transaccion_id: str,
        nombre: str,
        dni: str,
        email: str,
        telefono: str,
        producto: str,
        monto: float,
        chances: int,
        tickets: List[str],
        medio_pago: str = "mercadopago",
        estado: str = "Aprobado"
    ) -> Tuple[bool, str]:
        """
        Registra la fila con los datos del participante.
        Si Google Sheets está conectado, escribe en la nube.
        Si no, respalda en CSV local.
        """
        ahora = datetime.now()
        fecha_str = ahora.strftime("%Y-%m-%d")
        hora_str = ahora.strftime("%H:%M:%S")
        tickets_str = ", ".join(tickets)

        fila = [
            fecha_str,
            hora_str,
            transaccion_id,
            nombre,
            dni,
            email,
            telefono,
            producto,
            str(monto),
            str(chances),
            tickets_str,
            medio_pago,
            estado
        ]

        # 1. Intentar registrar en Google Sheets si está activo
        if self.is_connected and self.client:
            try:
                try:
                    sheet = self.client.open(SPREADSHEET_NAME)
                except Exception:
                    # Si no existe la planilla, intentar crearla
                    sheet = self.client.create(SPREADSHEET_NAME)
                
                try:
                    worksheet = sheet.worksheet(WORKSHEET_NAME)
                except Exception:
                    worksheet = sheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
                    worksheet.append_row(SHEET_HEADERS)

                # Verificar si tiene encabezados
                existing_rows = worksheet.get_all_values()
                if not existing_rows:
                    worksheet.append_row(SHEET_HEADERS)

                worksheet.append_row(fila)
                logger.info(f"Registro guardado exitosamente en Google Sheets para '{nombre}'.")
                return True, "google_sheets"
            except Exception as e:
                logger.error(f"Falla al escribir en Google Sheets: {e}. Guardando respaldo local...")

        # 2. Respaldo local en CSV si Google Sheets no está disponible
        self._guardar_en_csv_local(fila)
        return False, "local_backup_csv"

    def _guardar_en_csv_local(self, fila: List[str]):
        """Guarda la fila en el archivo CSV de respaldo para no perder ninguna compra"""
        existe_archivo = BACKUP_CSV_FILE.exists()

        try:
            with open(BACKUP_CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not existe_archivo:
                    writer.writerow(SHEET_HEADERS)
                writer.writerow(fila)
            logger.info(f"Registro respaldado localmente en {BACKUP_CSV_FILE.name}")
        except Exception as e:
            logger.error(f"Error escribiendo en respaldo local CSV: {e}")

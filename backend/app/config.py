import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuración de Google Sheets
CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Sorteo Auto 0KM - Participantes")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "Participantes")

# Mercado Pago / Pasarela de Pago
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "TEST_ACCESS_TOKEN_EJEMPLO")
MP_PUBLIC_KEY = os.getenv("MP_PUBLIC_KEY", "TEST_PUBLIC_KEY_EJEMPLO")

# Archivo de respaldo local
BACKUP_CSV_FILE = Path(__file__).resolve().parent.parent / "participantes_local_backup.csv"

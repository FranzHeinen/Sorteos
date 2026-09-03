import gspread
from google.oauth2.service_account import Credentials
import os

# Configuración
CREDENTIALS_FILE = 'credentials.json' # Asegurate de que el archivo se llame así
SPREADSHEET_NAME = 'Sorteo Auto 0KM - Participantes' # Debe coincidir exactamente con el nombre de tu archivo en Google Drive

def test_connection():
    try:
        # Credenciales
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Intentar abrir la planilla
        sheet = client.open(SPREADSHEET_NAME)
        print(f"✅ ¡Conexión exitosa!")
        print(f"Planilla encontrada: {sheet.title}")
        print(f"URL de la planilla: {sheet.url}")
        
    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    test_connection()
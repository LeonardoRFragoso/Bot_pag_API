import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Constantes
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')
USERS_DB_PATH = 'users.json'
TAXA_PERCENTUAL = 5.0  # Taxa de 5% sobre os produtos

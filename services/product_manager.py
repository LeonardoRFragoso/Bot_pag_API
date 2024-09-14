from services.db_manager import get_connection
from typing import List, Dict

def get_all_products() -> List[Dict[str, str]]:
    """Retorna a lista de todos os produtos cadastrados no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, preco FROM produtos")
    products = cursor.fetchall()

    conn.close()

    return [{"id": row[0], "nome": row[1], "preco": row[2]} for row in products]


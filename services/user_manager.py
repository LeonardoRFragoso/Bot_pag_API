import sqlite3
from typing import Optional  # Adicione isso para corrigir o erro
from services.db_manager import get_connection
from utils.logger import logger

class UserManager:
    """Gerencia usuários e suas informações com o banco de dados SQLite."""

    def register_user(self, user_id: int) -> bool:
        """Registra um novo usuário, se ele ainda não existir."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Verificar se o usuário já existe
            cursor.execute("SELECT id FROM usuarios WHERE user_id = ?", (user_id,))
            user_exists = cursor.fetchone()

            if not user_exists:
                cursor.execute("INSERT INTO usuarios (user_id) VALUES (?)", (user_id,))
                conn.commit()
                logger.info(f"Novo usuário {user_id} registrado com sucesso.")
                return True
            else:
                logger.info(f"Usuário {user_id} já está registrado.")
                return False

        except sqlite3.Error as e:
            logger.error(f"Erro ao registrar o usuário {user_id}: {e}")
        finally:
            conn.close()

    def get_user_email(self, user_id: int) -> Optional[str]:
        """Retorna o e-mail do Mercado Pago do usuário, se configurado."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT mercado_pago_email FROM usuarios WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()

            if user and user[0]:
                logger.info(f"E-mail do Mercado Pago do usuário {user_id} encontrado.")
                return user[0]
            else:
                logger.warning(f"E-mail do Mercado Pago para o usuário {user_id} não está configurado.")
                return None

        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar e-mail do Mercado Pago do usuário {user_id}: {e}")
        finally:
            conn.close()

    def set_user_email(self, user_id: int, email: str) -> None:
        """Define o e-mail do Mercado Pago de um usuário."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE usuarios SET mercado_pago_email = ? WHERE user_id = ?", (email, user_id))
            conn.commit()

            logger.info(f"E-mail do Mercado Pago {email} configurado para o usuário {user_id}.")

        except sqlite3.Error as e:
            logger.error(f"Erro ao configurar o e-mail do Mercado Pago para o usuário {user_id}: {e}")
        finally:
            conn.close()

    def get_all_products(self) -> list:
        """Retorna a lista de todos os produtos disponíveis para compra."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, preco FROM produtos")
            produtos = cursor.fetchall()

            # Formatar os produtos em um dicionário para facilitar o manuseio
            produtos_formatados = [{"id": produto[0], "nome": produto[1], "preco": produto[2]} for produto in produtos]
            
            logger.info("Produtos carregados com sucesso.")
            return produtos_formatados

        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar produtos: {e}")
            return []
        finally:
            conn.close()

    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        """Retorna os detalhes de um produto específico pelo ID."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, preco FROM produtos WHERE id = ?", (product_id,))
            produto = cursor.fetchone()

            if produto:
                logger.info(f"Produto {produto[1]} encontrado.")
                return {"id": produto[0], "nome": produto[1], "preco": produto[2]}
            else:
                logger.warning(f"Produto {product_id} não encontrado.")
                return None

        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar produto {product_id}: {e}")
            return None
        finally:
            conn.close()

# Instância global do gerenciador de usuários
user_manager = UserManager()

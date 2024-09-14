from telegram import Update
from telegram.ext import ContextTypes
from services.payment import process_payment
from utils.logger import logger

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para lidar com a seleção dos botões interativos."""
    query = update.callback_query
    await query.answer()

    # Obtendo o ID do usuário que interagiu com o botão
    user_id = str(query.from_user.id)
    logger.info(f"Usuário {user_id} selecionou um produto.")

    try:
        # O callback data contém o ID do produto (ajuste de índice para começar de 0)
        produto_id = int(query.data) - 1  
        logger.info(f"Produto ID {produto_id} selecionado para processamento.")
        
        # Passando o user_id e o produto_id corretos para o process_payment
        await process_payment(query, context, produto_id)
        
    except (ValueError, IndexError) as e:
        logger.error(f"Erro ao processar a seleção do produto: {e}")
        await query.message.reply_text('Houve um erro ao processar a seleção do produto.')

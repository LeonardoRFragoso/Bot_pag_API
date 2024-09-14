from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import commands, callbacks
from config import TELEGRAM_TOKEN
from utils.logger import logger

def main():
    """Ponto de entrada principal do bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adiciona handlers de comando
    application.add_handler(CommandHandler("start", commands.start))  # Comando para iniciar o bot e cadastrar o usuário
    application.add_handler(CommandHandler("listar_produtos", commands.listar_produtos))  # Listar produtos disponíveis
    application.add_handler(CommandHandler("fazer_pedido", commands.fazer_pedido))  # Fazer pedido e gerar QR code

    # Handler para botões interativos (callback queries)
    application.add_handler(CallbackQueryHandler(callbacks.button_handler))

    logger.info("Bot iniciado.")
    application.run_polling()

if __name__ == '__main__':
    main()

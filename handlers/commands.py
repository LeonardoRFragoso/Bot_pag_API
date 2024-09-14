from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_manager import user_manager
from services.payment import process_payment
from utils.logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para registrar o usuário e exibir comandos disponíveis."""
    user_id = update.message.from_user.id
    
    # Registra o usuário se ainda não estiver registrado
    if user_manager.register_user(user_id):
        await update.message.reply_text(
            'Cadastro realizado com sucesso! Aqui estão os comandos disponíveis:\n'
            '/listar_produtos - Listar produtos para compra'
        )
        logger.info(f"Novo usuário cadastrado: {user_id}")
    else:
        await update.message.reply_text(
            'Você já está cadastrado! Aqui estão os comandos disponíveis:\n'
            '/listar_produtos - Listar produtos para compra'
        )
        logger.info(f"Usuário já cadastrado: {user_id}")

async def listar_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para listar todos os produtos disponíveis."""
    user_id = update.message.from_user.id
    
    # Obtém todos os produtos disponíveis
    produtos = user_manager.get_all_products()
    
    if not produtos:
        await update.message.reply_text('Nenhum produto disponível no momento.')
        logger.info(f"Usuário {user_id} tentou listar produtos, mas não há produtos disponíveis.")
        return

    # Criação de botões interativos para os produtos
    keyboard = [
        [InlineKeyboardButton(f"{produto['nome']} - R${produto['preco']:.2f}", callback_data=str(produto['id']))]
        for produto in produtos
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('Escolha um produto para gerar o QR Code de pagamento:', reply_markup=reply_markup)
    logger.info(f"Usuário {user_id} listou produtos.")

async def fazer_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para fazer um pedido e gerar o link de pagamento"""
    user_id = update.message.from_user.id
    logger.info(f"Usuário {user_id} iniciou o comando /fazer_pedido")

    if len(context.args) < 1:
        await update.message.reply_text('Uso: /fazer_pedido <ID do produto>')
        logger.warning(f"Argumentos insuficientes para o comando /fazer_pedido. Recebido: {context.args}")
        return

    try:
        produto_id = int(context.args[0])
        logger.info(f"Processando pedido. Produto ID: {produto_id}")
    except ValueError:
        await update.message.reply_text('Uso: /fazer_pedido <ID do produto>')
        logger.error(f"Erro ao processar os argumentos do pedido: {context.args}")
        return

    # Verificar se o produto existe
    produto = user_manager.get_product_by_id(produto_id)
    if not produto:
        logger.error(f"Produto {produto_id} não encontrado.")
        await update.message.reply_text('Produto não encontrado.')
        return

    # Verificar se o vendedor do produto tem e-mail do Mercado Pago configurado
    vendedor_email = user_manager.get_user_email(user_id)
    if not vendedor_email:
        logger.error(f"Vendedor {user_id} não configurou o email do Mercado Pago.")
        await update.message.reply_text('Vendedor não configurou a conta do Mercado Pago.')
        return

    # Processar pagamento (chamar função do arquivo payment.py)
    await process_payment(update, context, produto_id)

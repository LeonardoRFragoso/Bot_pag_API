import os
import base64
from typing import Dict, Optional, Any
from telegram import Update
from telegram.ext import ContextTypes
from services.user_manager import user_manager
from utils.logger import logger
from config import TAXA_PERCENTUAL
import mercadopago

# Inicialização do SDK do Mercado Pago usando o token da variável de ambiente
sdk = mercadopago.SDK(os.getenv('MERCADO_PAGO_ACCESS_TOKEN'))

def criar_pagamento(vendedor_email: str, produto: Dict[str, Any], taxa_percentual: float) -> Optional[Dict[str, Any]]:
    """Cria um pagamento no Mercado Pago e retorna a resposta da API."""
    try:
        logger.info(f"Iniciando criação de pagamento para o produto: {produto['nome']} com o email do vendedor: {vendedor_email}")
        
        preco_produto = produto["preço"]
        taxa = preco_produto * (taxa_percentual / 100)
        total = preco_produto + taxa

        pagamento = {
            "transaction_amount": total,
            "description": f"Pagamento por {produto['nome']}",
            "payment_method_id": "pix",
            "payer": {"email": "comprador@example.com"},  # Email fictício
            "external_reference": vendedor_email
        }

        pagamento_resposta = sdk.payment().create(pagamento)
        logger.info(f"Resposta da API do Mercado Pago: {pagamento_resposta}")

        if pagamento_resposta.get("status") != 201:
            logger.error(f"Erro na criação do pagamento: {pagamento_resposta}")
            return None

        return pagamento_resposta
    except Exception as e:
        logger.error(f"Erro ao criar pagamento no Mercado Pago: {e}")
        return None

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, produto_id: int, user_id: str) -> None:
    """Processa o pagamento do produto escolhido."""
    logger.info(f"Processando pagamento para o usuário {user_id}")

    vendedor_email = user_manager.get_user_email(user_id)

    if not vendedor_email:
        await update.message.reply_text('Vendedor não configurou a conta do Mercado Pago.')
        logger.error(f"Vendedor {user_id} não configurou o email do Mercado Pago.")
        return

    produtos = user_manager.get_products(user_id)
    if not produtos or produto_id >= len(produtos):
        await update.message.reply_text('Produto não encontrado.')
        logger.error(f"Produto {produto_id} não encontrado para o vendedor {user_id}.")
        return

    produto = produtos[produto_id]
    pagamento_resposta = criar_pagamento(vendedor_email, produto, TAXA_PERCENTUAL)

    if not pagamento_resposta:
        await update.message.reply_text('Houve um problema ao processar o pagamento.')
        logger.error("Erro na resposta do Mercado Pago ou pagamento_resposta é None.")
        return

    try:
        transaction_data = pagamento_resposta["response"]["point_of_interaction"]["transaction_data"]
        ticket_url = transaction_data.get("ticket_url")
        qr_code_base64 = transaction_data.get("qr_code_base64")

        if ticket_url and qr_code_base64:
            qr_code_bytes = base64.b64decode(qr_code_base64)
            await update.message.reply_photo(photo=qr_code_bytes, caption=f'Este é o QR code para pagamento via PIX. {ticket_url}')
            logger.info(f"QR code e link de pagamento enviados com sucesso para o produto {produto['nome']}.")
        else:
            logger.error("Faltam informações no ticket_url ou qr_code_base64.")
            await update.message.reply_text('Informações de pagamento incompletas.')
    except KeyError as e:
        logger.error(f"Erro ao acessar informações da resposta da API: {e}")
        await update.message.reply_text('Erro ao processar os dados do pagamento.')
    except Exception as e:
        logger.error(f"Erro ao processar o pagamento: {e}")
        await update.message.reply_text('Erro inesperado ao processar o pagamento.')

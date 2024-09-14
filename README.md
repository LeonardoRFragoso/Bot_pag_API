# Projeto Bot de Pagamentos com Telegram e Mercado Pago

Este projeto é um bot de Telegram desenvolvido para processar pagamentos via Mercado Pago. Os usuários podem interagir com o bot para visualizar produtos disponíveis e gerar QR codes de pagamento para compra.

## Funcionalidades

- Registro de usuários
- Listagem de produtos para compra
- Integração com a API do Mercado Pago para gerar QR codes de pagamento via PIX
- Persistência de dados utilizando SQLite

## Tecnologias Utilizadas

- **Python**: Linguagem principal usada no desenvolvimento
- **Python-Telegram-Bot**: Framework usado para a criação do bot de Telegram
- **Mercado Pago SDK**: Usado para integrar a funcionalidade de pagamentos via PIX
- **SQLite**: Banco de dados utilizado para persistência de dados
- **httpx**: Biblioteca para fazer requisições HTTP
- **dotenv**: Para gerenciar variáveis de ambiente

## Instalação

### Pré-requisitos

Certifique-se de que você tem o Python 3.10+ instalado.

### Passos

1. Clone o repositório:
    ```bash
    git clone https://github.com/LeonardoRFragoso/Bot_pag_API/
    cd seu-repositorio
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o arquivo `.env` com suas credenciais do Telegram e Mercado Pago:
    ```
    TELEGRAM_TOKEN=seu-token-do-telegram
    MERCADO_PAGO_ACCESS_TOKEN=seu-token-do-mercado-pago
    ```

5. Crie o banco de dados SQLite e as tabelas necessárias:
    ```bash
    sqlite3 bot_database.db
    ```
    Execute os seguintes comandos SQL dentro do terminal do SQLite:
    ```sql
    -- Criação da tabela de usuários
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE NOT NULL,
        mercado_pago_email TEXT
    );

    -- Criação da tabela de produtos
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL
    );
    ```

6. Adicione um usuário e produtos de teste:
    ```sql
    -- Inserir um usuário de teste
    INSERT INTO usuarios (user_id, mercado_pago_email)
    VALUES ('833732395', 'seuemail@mercadopago.com');

    -- Inserir alguns produtos de teste
    INSERT INTO produtos (nome, preco)
    VALUES
        ('Produto 1', 100.0),
        ('Produto 2', 200.0),
        ('Produto 3', 300.0);
    ```

7. Execute o bot:
    ```bash
    python app.py
    ```

## Comandos Disponíveis

- `/start`: Registra o usuário e exibe os comandos disponíveis
- `/listar_produtos`: Lista os produtos disponíveis para compra
- `/fazer_pedido <ID do produto>`: Gera um QR code para o produto escolhido

## Estrutura do Projeto

```shell
├── app.py               # Arquivo principal do bot
├── handlers/            # Diretório com os manipuladores de comandos e callbacks
├── services/            # Diretório com serviços como UserManager, PaymentManager
├── utils/               # Utilitários como logging e funções auxiliares
├── bot_database.db      # Arquivo do banco de dados SQLite
├── .env                 # Variáveis de ambiente
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo

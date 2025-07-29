import asyncio
import websockets
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Um conjunto para armazenar todos os clientes conectados
CONNECTED_CLIENTS = set()

async def handler(websocket):
    """
    Gerencia uma conexão de cliente WebSocket.
    """
    logging.info(f"Cliente conectado: {websocket.remote_address}")
    CONNECTED_CLIENTS.add(websocket)
    try:
        # Fica escutando por mensagens do cliente
        async for message in websocket:
            logging.info(f"Mensagem recebida de {websocket.remote_address}: {message}")
            
            # Prepara a mensagem para ser enviada aos outros clientes
            formatted_message = f"[{websocket.remote_address[0]}:{websocket.remote_address[1]}]: {message}"
            
            # Envia a mensagem para todos os clientes conectados
            websockets.broadcast(CONNECTED_CLIENTS, formatted_message)
            
    except websockets.exceptions.ConnectionClosedError:
        logging.info(f"Cliente desconectado (erro): {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedOK:
        logging.info(f"Cliente desconectado (normal): {websocket.remote_address}")
    finally:
        # Remove o cliente do conjunto ao desconectar
        CONNECTED_CLIENTS.remove(websocket)


async def main():
    """
    Inicia o servidor WebSocket.
    """
    host = "localhost"
    port = 8765
    async with websockets.serve(handler, host, port):
        logging.info(f"Servidor WebSocket iniciado em ws://{host}:{port}")
        await asyncio.Future()  # Mantém o servidor rodando indefinidamente

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor desligado.")

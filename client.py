import asyncio
import websockets
import aioconsole
import sys

async def receive_messages(websocket):
    """
    Ouve continuamente as mensagens do servidor e as imprime.
    """
    try:
        async for message in websocket:
            print(f"\r{message}\n> ", end="")
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor perdida.")

async def send_messages(websocket):
    """
    Lê a entrada do usuário do terminal e a envia para o servidor.
    """
    while True:
        message = await aioconsole.ainput("> ")
        if message.lower() == 'exit':
            break
        await websocket.send(message)

async def main(uri):
    """
    Função principal para conectar e gerenciar as tarefas do cliente.
    """
    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado ao servidor de chat. Digite 'exit' para sair.")
            
            # Executa as tarefas de envio e recebimento concorrentemente
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))

            # Aguarda a conclusão de qualquer uma das tarefas
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancela as tarefas pendentes para garantir um desligamento limpo
            for task in pending:
                task.cancel()
                
    except ConnectionRefusedError:
        print(f"Erro: Conexão recusada. O servidor está rodando em {uri}?")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python client.py <ws_uri>")
        print("Exemplo local: python client.py ws://localhost:8765")
        sys.exit(1)
        
    # Para o cliente funcionar, também é necessário instalar aioconsole
    # pip install aioconsole
    uri = sys.argv[1]
    asyncio.run(main(uri))
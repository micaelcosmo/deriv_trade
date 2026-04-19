import asyncio
import websockets
import socket

# Forçar IPv4
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

async def test_connection(url):
    print(f"Testando IPv4 para: {url}")
    try:
        async with websockets.connect(url, ping_interval=None) as ws:
            print("  -> Sucesso")
    except Exception as e:
        print(f"  -> Falha: {e}")

async def main():
    await test_connection("wss://ws.binaryws.com/websockets/v3?app_id=1089")

if __name__ == "__main__":
    asyncio.run(main())

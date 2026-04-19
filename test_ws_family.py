import asyncio
import websockets
import socket

async def test_connection(url):
    print(f"Testando family=socket.AF_INET para: {url}")
    try:
        async with websockets.connect(url, family=socket.AF_INET, ping_interval=None) as ws:
            print("  -> Sucesso")
    except Exception as e:
        print(f"  -> Falha: {e}")

async def main():
    await test_connection("wss://ws.binaryws.com/websockets/v3?app_id=1089")

if __name__ == "__main__":
    asyncio.run(main())

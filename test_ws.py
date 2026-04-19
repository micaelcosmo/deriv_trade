import asyncio
import websockets

async def test_connection(url):
    print(f"Testando: {url}")
    try:
        async with websockets.connect(url, ping_interval=None) as ws:
            print("  -> Sucesso")
    except Exception as e:
        print(f"  -> Falha: {e}")

async def main():
    urls = [
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
        "wss://ws.derivws.com/websockets/v3?app_id=1089",
        "wss://frontend.binaryws.com/websockets/v3?app_id=1089"
    ]
    for url in urls:
        await test_connection(url)

if __name__ == "__main__":
    asyncio.run(main())

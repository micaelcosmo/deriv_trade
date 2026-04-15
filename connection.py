import json
import websockets

from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class DerivClient:
    """Responsável exclusivo por gerenciar a conexão com a API da Deriv."""

    def __init__(self, api_url):
        self.api_url = api_url
        self.ws = None

    async def connect(self):
        """Estabelece a conexão WebSocket."""
        logger.info(f"Estabelecendo conexão com {self.api_url}...")
        self.ws = await websockets.connect(self.api_url)
        logger.info("Conexão WebSocket estabelecida com sucesso.")

    async def send(self, payload: dict):
        """Envia um dicionário como JSON para a API."""
        await self.ws.send(json.dumps(payload))

    async def receive(self):
        """Aguarda e retorna a próxima mensagem da API como dicionário."""
        response = await self.ws.recv()
        return json.loads(response)

    async def authenticate(self, token: str):
        """Realiza a autenticação utilizando o token de Trade."""
        logger.info("Enviando requisição de autenticação...")
        await self.send({"authorize": token})
        
        while True:
            response = await self.receive()
            if "error" in response:
                error_msg = response['error']['message']
                logger.error(f"Erro de Autenticação: {error_msg}")
                raise PermissionError(error_msg)
            
            if "authorize" in response:
                auth_data = response["authorize"]
                logger.info(f"Autenticado! Email: {auth_data['email']} | Saldo: {auth_data['balance']} {auth_data['currency']}")
                return auth_data
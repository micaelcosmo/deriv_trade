from connection import DerivClient
from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class TradingEngine:
    """Engine de comunicação com os contratos e histórico da corretora."""

    def __init__(self, client: DerivClient):
        self.client = client

    async def get_tick_history(self, symbol: str, count: int = 3) -> list[float]:
        """Busca o histórico público do ativo sem precisar de autenticação."""
        logger.info(f"Buscando histórico dos últimos {count} preços para {symbol}...")
        
        await self.client.send({
            "ticks_history": symbol,
            "end": "latest",
            "count": count
        })
        
        while True:
            response = await self.client.receive()
            if "error" in response:
                error_msg = response['error']['message']
                logger.error(f"Erro ao buscar histórico: {error_msg}")
                raise ValueError(error_msg)
            
            if "history" in response:
                prices = response["history"]["prices"]
                float_prices = [float(p) for p in prices]
                logger.info(f"Histórico recebido: {float_prices}")
                return float_prices

    async def execute_trade(self, symbol: str, contract_type: str, amount: float, duration: int, duration_unit: str):
        """Executa a compra ou venda do contrato."""
        logger.info(f"Preparando ordem: {contract_type} de ${amount} em {symbol} ({duration}{duration_unit}).")
        
        payload = {
            "buy": 1,
            "price": amount,
            "parameters": {
                "amount": amount,
                "basis": "stake",
                "contract_type": contract_type,
                "currency": "USD",
                "duration": duration,
                "duration_unit": duration_unit,
                "symbol": symbol
            }
        }
        await self.client.send(payload)
        
        while True:
            response = await self.client.receive()
            if "error" in response:
                logger.error(f"Erro na execução da ordem: {response['error']['message']}")
                return None
            
            if "buy" in response:
                buy_data = response["buy"]
                logger.info(f"Ordem aceita! ID do Contrato: {buy_data['contract_id']}.")
                return buy_data

    async def wait_for_result(self, contract_id: int):
        """Acompanha o contrato aberto até o fechamento e retorna o resultado."""
        logger.info(f"Aguardando resultado para o contrato {contract_id}...")
        
        await self.client.send({
            "proposal_open_contract": 1,
            "contract_id": contract_id,
            "subscribe": 1
        })
        
        while True:
            response = await self.client.receive()
            if "proposal_open_contract" in response:
                contract = response["proposal_open_contract"]
                
                if contract.get("is_sold"):
                    profit = float(contract.get("profit", 0))
                    status = "WIN" if profit > 0 else "LOSS"
                    logger.info(f"Contrato finalizado. Status: {status} | P&L: ${profit}")
                    return {"status": status, "profit": profit}
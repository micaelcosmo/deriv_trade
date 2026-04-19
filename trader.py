from connection import DerivClient
from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class TradingEngine:
    """Engine de comunicação com os contratos e histórico da corretora."""

    def __init__(self, client: DerivClient, socketio=None):
        self.client = client
        self.socketio = socketio

    async def get_candle_history(self, symbol: str, count: int = 5, timeframe_seconds: int = 60) -> list[dict]:
        """Busca o histórico de candles do ativo sem precisar de autenticação."""
        logger.info(f"Buscando histórico dos últimos {count} candles de {timeframe_seconds}s para {symbol}...")
        
        await self.client.send({
            "ticks_history": symbol,
            "end": "latest",
            "count": count,
            "style": "candles",
            "granularity": timeframe_seconds
        })
        
        while True:
            response = await self.client.receive()
            if "error" in response:
                error_msg = response['error']['message']
                logger.error(f"Erro ao buscar histórico de candles: {error_msg}")
                raise ValueError(error_msg)
            
            if "candles" in response:
                candles = response.get("candles", [])
                logger.info(f"Histórico de {len(candles)} candles recebido.")
                
                # Emitir para o dashboard em tempo real
                if self.socketio:
                    self.socketio.emit('chart_data', candles)
                
                return candles

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
        logger.info("Inscrevendo em atualizações do contrato...")
        
        await self.client.send({
            "proposal_open_contract": 1,
            "contract_id": contract_id,
            "subscribe": 1
        })
        
        max_attempts = 300  # ~5 minutos com timeout
        attempts = 0
        
        while attempts < max_attempts:
            try:
                response = await self.client.receive()
                
                if "error" in response:
                    logger.error(f"Erro ao acompanhar contrato: {response['error']['message']}")
                    return None
                
                if "proposal_open_contract" in response:
                    contract = response["proposal_open_contract"]
                    current_spot = contract.get("current_spot", "N/A")
                    entry_spot = contract.get("entry_spot", "N/A")
                    is_sold = contract.get("is_sold", False)
                    
                    if is_sold:
                        profit = float(contract.get("profit", 0))
                        payout = float(contract.get("payout", 0))
                        status = "WIN ✓" if profit > 0 else "LOSS ✗"
                        logger.info("=" * 50)
                        logger.info(f"CONTRATO FINALIZADO!")
                        logger.info(f"Status: {status}")
                        logger.info(f"Entrada: ${entry_spot}")
                        logger.info(f"Saída: ${current_spot}")
                        logger.info(f"P&L: ${profit}")
                        logger.info(f"Payout: ${payout}")
                        logger.info("=" * 50)
                        return {"status": status.split()[0], "profit": profit, "payout": payout}
                    else:
                        # Contrato ainda aberto
                        logger.info(f"Contrato aberto - Entrada: ${entry_spot}, Spot atual: ${current_spot}")
                
                attempts += 1
                
            except Exception as e:
                logger.error(f"Erro ao processar resposta: {e}")
                attempts += 1
        
        logger.error("Timeout ao aguardar resultado do contrato")
        return None
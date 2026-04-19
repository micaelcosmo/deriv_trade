import asyncio

from config import Config
from connection import DerivClient
from trader import TradingEngine
from strategy import ContrarianStrategy
from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class BotRunner:
    """Orquestrador do bot."""

    def __init__(self, socketio=None):
        self.client = DerivClient(Config.API_URL)
        self.trader = TradingEngine(self.client, socketio=socketio)
        self.strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=Config.MIN_AVG_CANDLE_BODY_SIZE)
        self.socketio = socketio

    async def run(self):
        logger.info("--- Iniciando Bot de Trading de Criptomoedas ---")
        
        await self.client.connect()

        # 1. Coleta de dados de mercado (candles de 1 minuto)
        candles = await self.trader.get_candle_history(Config.SYMBOL, count=5, timeframe_seconds=60)
        
        # Emitir dados do gráfico para o frontend
        if self.socketio and candles:
            self.socketio.emit('chart_data', candles)

        # 2. Tomada de decisão lógica
        signal, reason = self.strategy.analyze(candles)
        
        if not signal:
            logger.warning(f"Nenhuma operação realizada para {Config.SYMBOL}. Motivo: {reason}")
            logger.info("--- Ciclo do Bot Encerrado ---")
            return

        logger.info(f"Oportunidade detectada! Motivo: {reason}")
        logger.info(f"Sinal de Operação: {signal}")
        
        if Config.TEST_MODE:
            # Modo teste: simula a operação
            logger.warning("=" * 40)
            logger.warning("MODO TESTE ATIVADO")
            logger.warning("=" * 40)
            logger.info(f"Sinal: {signal}")
            logger.info(f"Motivo: {reason}")
            logger.info(f"Valor: ${Config.STAKE}")
            logger.info(f"Duração: {Config.DURATION}{Config.DURATION_UNIT}")
            logger.warning("(Nenhum trade executado)")
            logger.warning("=" * 40)
        else:
            # Modo real: executa o trade
            try:
                logger.info("Autenticando na corretora para executar a ordem...")
                await self.client.authenticate(Config.TOKEN)

                # 4. Execução da ordem
                logger.info(f"Executando ordem: {signal} de ${Config.STAKE}")
                buy_receipt = await self.trader.execute_trade(
                    symbol=Config.SYMBOL, 
                    contract_type=signal, 
                    amount=Config.STAKE,
                    duration=Config.DURATION,
                    duration_unit=Config.DURATION_UNIT
                )
                
                if not buy_receipt:
                    logger.error("Falha ao comprar contrato. Encerrando o ciclo.")
                    return

                contract_id = buy_receipt["contract_id"]
                
                # 5. Colheita de resultados
                result = await self.trader.wait_for_result(contract_id)
                
                if result:
                    logger.info("Resultado armazenado com sucesso.")
                else:
                    logger.error("Falha ao obter resultado do contrato.")
                    
            except PermissionError as e:
                logger.error(f"Erro de autenticação: {e}")
                logger.info("Verifique seu token na configuração.")
            except Exception as e:
                logger.error(f"Erro ao executar trade: {e}")
                logger.error(f"Tipo do erro: {type(e).__name__}")
        
        logger.info("--- Ciclo do Bot Encerrado ---")
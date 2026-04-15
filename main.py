import asyncio

from config import Config
from connection import DerivClient
from trader import TradingEngine
from strategy import TrendStrategy
from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class BotRunner:
    """Orquestrador do bot."""

    def __init__(self):
        self.client = DerivClient(Config.API_URL)
        self.trader = TradingEngine(self.client)
        self.strategy = TrendStrategy(period=3)

    async def run(self):
        logger.info("--- Iniciando Bot de Trading de Criptomoedas ---")
        
        await self.client.connect()

        # 1. Leitura de mercado via endpoint público (Bypassa a exigência de token)
        history = await self.trader.get_tick_history(Config.SYMBOL, count=3)
        for price in history:
            self.strategy.add_tick(price)

        # 2. Tomada de decisão lógica
        signal = self.strategy.get_signal()
        
        if not signal:
            logger.warning(f"Mercado sem tendência clara para {Config.SYMBOL}. Nenhuma operação realizada.")
            logger.info("--- Ciclo do Bot Encerrado ---")
            return

        logger.info(f"Lógica Matemática detectou oportunidade: {signal} em {Config.SYMBOL}!")
        
        # 3. Autenticação apenas para execução da ordem (Exige apenas o token 'Trade')
        logger.info("Autenticando na corretora para executar a ordem...")
        await self.client.authenticate(Config.TOKEN)

        # 4. Execução da ordem
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
        
        logger.info("=" * 40)
        logger.info(f"RESULTADO FINAL: {result['status']}")
        logger.info(f"LUCRO/PREJUÍZO: ${result['profit']}")
        logger.info("=" * 40)
        logger.info("--- Ciclo do Bot Encerrado ---")


if __name__ == "__main__":
    bot = BotRunner()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.warning("Bot interrompido manualmente pelo usuário.")
    except Exception as e:
        logger.critical(f"Erro inesperado: {str(e)}")
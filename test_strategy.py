import pytest
from unittest.mock import AsyncMock

from strategy import ContrarianStrategy
from trader import TradingEngine
from connection import DerivClient


# Dados de candle de exemplo para os testes
# Formato: {'open': o, 'close': c} (high/low não são usados na lógica atual)
CANDLES_MAJORITY_SELL = [
    {'open': 10, 'close': 8},   # Sell
    {'open': 8, 'close': 9},    # Buy
    {'open': 9, 'close': 7},    # Sell
    {'open': 7, 'close': 6},    # Sell
    {'open': 6, 'close': 6.5},  # Buy
] # 3 Sell, 2 Buy -> Sinal esperado: CALL

CANDLES_MAJORITY_BUY = [
    {'open': 10, 'close': 11},  # Buy
    {'open': 11, 'close': 10},  # Sell
    {'open': 10, 'close': 12},  # Buy
    {'open': 12, 'close': 13},  # Buy
    {'open': 13, 'close': 12.5},# Sell
] # 3 Buy, 2 Sell -> Sinal esperado: PUT

CANDLES_EQUILIBRIUM = [
    {'open': 10, 'close': 11},  # Buy
    {'open': 11, 'close': 10},  # Sell
    {'open': 10, 'close': 12},  # Buy
    {'open': 12, 'close': 11},  # Sell
    {'open': 11, 'close': 11},  # Doji/Neutral
] # 2 Buy, 2 Sell -> Sinal esperado: None

CANDLES_LOW_VOLATILITY = [
    {'open': 10.0, 'close': 10.1},
    {'open': 10.1, 'close': 10.0},
    {'open': 10.0, 'close': 10.1},
    {'open': 10.1, 'close': 10.2},
    {'open': 10.2, 'close': 10.1},
] # Corpos muito pequenos, volatilidade baixa


class TestContrarianStrategy:
    """Suíte de testes para a nova estratégia contrária com análise de candles."""

    def test_not_enough_data(self):
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=0.5)
        signal, reason = strategy.analyze(CANDLES_MAJORITY_BUY[:3]) # Apenas 3 candles
        assert signal is None
        assert "Dados insuficientes" in reason

    def test_majority_sell_candles_gives_call_signal(self):
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=0.5)
        signal, reason = strategy.analyze(CANDLES_MAJORITY_SELL)
        assert signal == "CALL"
        assert "Maioria de Venda" in reason

    def test_majority_buy_candles_gives_put_signal(self):
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=0.5)
        signal, reason = strategy.analyze(CANDLES_MAJORITY_BUY)
        assert signal == "PUT"
        assert "Maioria de Compra" in reason

    def test_equilibrium_gives_no_signal(self):
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=0.5)
        signal, reason = strategy.analyze(CANDLES_EQUILIBRIUM)
        assert signal is None
        assert "equilibrados" in reason

    def test_low_volatility_gives_no_signal(self):
        # O tamanho médio do corpo aqui é (0.1+0.1+0.1+0.1+0.1)/5 = 0.1
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=0.5)
        signal, reason = strategy.analyze(CANDLES_LOW_VOLATILITY)
        assert signal is None
        assert "Baixa volatilidade" in reason

    def test_volatility_just_above_threshold(self):
        # O tamanho médio do corpo para CANDLES_MAJORITY_BUY é (1+1+2+1+0.5)/5 = 1.1
        strategy = ContrarianStrategy(period=5, min_avg_candle_body_size=1.0)
        signal, reason = strategy.analyze(CANDLES_MAJORITY_BUY)
        assert signal == "PUT" # Deve funcionar pois 1.1 > 1.0


class TestTradingEngine:
    """Suíte de testes para o TradingEngine, usando um cliente de API simulado (mock)."""

    @pytest.fixture
    def mock_client(self) -> AsyncMock:
        """Cria um mock assíncrono para o DerivClient para cada teste."""
        client = AsyncMock(spec=DerivClient)
        return client

    @pytest.mark.asyncio
    async def test_get_candle_history_success(self, mock_client: AsyncMock):
        """Testa o caminho de sucesso para a busca de candles."""
        # Setup: Configura o mock para retornar uma resposta de sucesso da API
        api_response = {"candles": [{'open': 100, 'close': 101}, {'open': 101, 'close': 102}]}
        mock_client.receive.return_value = api_response
        
        trader = TradingEngine(mock_client)

        # Execute: Chama o método que queremos testar
        candles = await trader.get_candle_history("cryBTCUSD", count=2, timeframe_seconds=60)

        # Assert: Verifica se o trader se comportou como esperado
        mock_client.send.assert_called_once() # Garante que uma requisição foi enviada
        assert candles == api_response["candles"]

    @pytest.mark.asyncio
    async def test_get_candle_history_api_error(self, mock_client: AsyncMock):
        """Testa se o trader lida corretamente com uma mensagem de erro da API."""
        # Setup: Configura o mock para retornar uma resposta de erro
        mock_client.receive.return_value = {"error": {"message": "Invalid symbol"}}
        trader = TradingEngine(mock_client)

        # Execute & Assert: Verifica se uma exceção específica foi levantada
        with pytest.raises(ValueError, match="Invalid symbol"):
            await trader.get_candle_history("invalid_symbol")

    @pytest.mark.asyncio
    async def test_execute_trade_success(self, mock_client: AsyncMock):
        """Testa o caminho de sucesso para a execução de uma ordem."""
        # Setup
        api_response = {"buy": {"contract_id": 12345, "payout": 1.95}}
        mock_client.receive.return_value = api_response
        trader = TradingEngine(mock_client)

        # Execute
        receipt = await trader.execute_trade("cryBTCUSD", "CALL", 10.0, 1, "m")

        # Assert
        mock_client.send.assert_called_once()
        assert receipt is not None
        assert receipt["contract_id"] == 12345

    @pytest.mark.asyncio
    async def test_wait_for_result_win(self, mock_client: AsyncMock):
        """Testa o acompanhamento de um contrato com resultado de vitória."""
        # Setup: Simula duas respostas da API: uma de "em andamento" e outra de "finalizado"
        mock_client.receive.side_effect = [
            {"proposal_open_contract": {"is_sold": 0}}, # Contrato ainda aberto
            {"proposal_open_contract": {"is_sold": 1, "profit": 9.5}} # Contrato vendido com lucro
        ]
        trader = TradingEngine(mock_client)

        # Execute
        result = await trader.wait_for_result(12345)

        # Assert
        # Garante que a subscrição foi enviada
        mock_client.send.assert_called_once_with({
            "proposal_open_contract": 1,
            "contract_id": 12345,
            "subscribe": 1
        })
        assert mock_client.receive.call_count == 2 # Garante que esperou pelas duas respostas
        assert result["status"] == "WIN"
        assert result["profit"] == 9.5
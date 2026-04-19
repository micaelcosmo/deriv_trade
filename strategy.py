class ContrarianStrategy:
    """
    Estratégia contrária baseada na maioria dos candles anteriores.
    Também inclui uma verificação de volatilidade mínima.
    """

    def __init__(self, period: int = 5, min_avg_candle_body_size: float = 0.0):
        """
        Inicializa a estratégia.
        :param period: Número de candles a serem analisados.
        :param min_avg_candle_body_size: O tamanho médio mínimo do corpo do candle para considerar o mercado volátil.
        """
        self.period = period
        self.min_avg_candle_body_size = min_avg_candle_body_size

    def analyze(self, candles: list[dict]) -> tuple[str | None, str]:
        """
        Analisa uma lista de candles.
        Retorna 'CALL' (Compra/Cima), 'PUT' (Venda/Baixo) ou None (Aguardar).
        Também retorna uma razão pela decisão.
        """
        if not candles or len(candles) < self.period:
            return None, f"Dados insuficientes ({len(candles)}/{self.period} candles)."

        # 1. Verificação de volatilidade (variação)
        candle_bodies = [abs(c['close'] - c['open']) for c in candles]
        avg_body_size = sum(candle_bodies) / len(candle_bodies)

        if avg_body_size < self.min_avg_candle_body_size:
            return None, f"Baixa volatilidade. Média do corpo do candle (${avg_body_size:.4f}) abaixo do mínimo (${self.min_avg_candle_body_size:.4f})."

        # 2. Lógica Contrária: contar candles de compra (verde) e venda (vermelho)
        buy_candles = sum(1 for c in candles if c['close'] > c['open'])
        sell_candles = sum(1 for c in candles if c['close'] < c['open'])

        if sell_candles > buy_candles:
            return "CALL", f"Sinal CONTRÁRIO: Maioria de Venda ({sell_candles}/{self.period}) -> Aposta em ALTA."
        elif buy_candles > sell_candles:
            return "PUT", f"Sinal CONTRÁRIO: Maioria de Compra ({buy_candles}/{self.period}) -> Aposta em BAIXA."
        else:
            return None, f"Mercado indeciso. Candles de compra ({buy_candles}) e venda ({sell_candles}) equilibrados."
class TrendStrategy:
    """
    Classe de domínio puro para análise de mercado cripto.
    Isolada de bibliotecas externas para permitir testes lógicos puros.
    """

    def __init__(self, period: int = 3):
        self.period = period
        self.history = []
        self.current_trend = None

    def add_tick(self, price: float):
        """Adiciona um novo preço ao histórico respeitando a janela de período."""
        self.history.append(price)
        if len(self.history) > self.period:
            self.history.pop(0)

    def get_signal(self) -> str | None:
        """
        Analisa o histórico.
        Retorna 'CALL' (Compra/Cima), 'PUT' (Venda/Baixo) ou None (Aguardar).
        """
        if len(self.history) < self.period:
            return None

        is_call = all(self.history[i] < self.history[i + 1] for i in range(len(self.history) - 1))
        if is_call:
            if self.current_trend != "CALL":
                self.current_trend = "CALL"
                return "CALL"
            return None

        is_put = all(self.history[i] > self.history[i + 1] for i in range(len(self.history) - 1))
        if is_put:
            if self.current_trend != "PUT":
                self.current_trend = "PUT"
                return "PUT"
            return None

        self.current_trend = None
        return None
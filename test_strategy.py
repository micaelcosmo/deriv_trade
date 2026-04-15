import pytest

from strategy import TrendStrategy


class TestTrendStrategy:
    """Suíte de testes puros para a lógica matemática de trade."""

    def test_add_tick_limits_history_size(self):
        strategy = TrendStrategy(period=3)
        strategy.add_tick(1.0)
        strategy.add_tick(2.0)
        strategy.add_tick(3.0)
        strategy.add_tick(4.0)
        
        assert len(strategy.history) == 3
        assert strategy.history == [2.0, 3.0, 4.0]

    def test_get_signal_not_enough_data(self):
        strategy = TrendStrategy(period=3)
        strategy.add_tick(10.0)
        strategy.add_tick(11.0)
        
        assert strategy.get_signal() is None

    def test_get_signal_call_trend(self):
        strategy = TrendStrategy(period=3)
        prices = [100.5, 101.0, 102.5]
        for price in prices:
            strategy.add_tick(price)
            
        assert strategy.get_signal() == "CALL"

    def test_get_signal_put_trend(self):
        strategy = TrendStrategy(period=3)
        prices = [50.0, 49.5, 48.0]
        for price in prices:
            strategy.add_tick(price)
            
        assert strategy.get_signal() == "PUT"

    def test_get_signal_no_trend_fluctuation(self):
        strategy = TrendStrategy(period=3)
        prices = [10.0, 12.0, 11.0]
        for price in prices:
            strategy.add_tick(price)
            
        assert strategy.get_signal() is None

    def test_no_repeated_signals_in_same_trend(self):
        strategy = TrendStrategy(period=3)
        prices = [1.0, 2.0, 3.0, 4.0, 5.0]
        signals = []
        
        for price in prices:
            strategy.add_tick(price)
            sig = strategy.get_signal()
            if sig:
                signals.append(sig)
                
        assert signals == ["CALL"]

    def test_integration_flow_multiple_signals(self):
        strategy = TrendStrategy(period=3)
        stream = [1.0, 2.0, 3.0, 2.5, 2.0, 1.5, 10.0, 11.0, 12.0]
        signals = []
        
        for price in stream:
            strategy.add_tick(price)
            sig = strategy.get_signal()
            if sig:
                signals.append(sig)
                
        assert signals == ["CALL", "PUT", "CALL"]
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SPY"
        
    @property
    def assets(self):
        return [self.ticker]
        
    @property
    def interval(self):
        return "1day"
        
    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {self.ticker: 0}
        
        # Ensure there's sufficient data to calculate indicators
        if len(data["ohlcv"]) < 50:  # Looking at 50 days to be safe for both short and long term averages
            return TargetAllocation(allocation_dict)
        
        # Calculate short term and long term moving averages
        short_term_sma = SMA(self.ticker, data["ohlcv"], length=20)[-1]  # 20-day SMA
        long_term_ema = EMA(self.ticker, data["ohlcv"], length=50)[-1]  # 50-day EMA
        
        # Determine allocation based on golden cross and death cross strategy
        if short_term_sma > long_term_ema:
            # If short-term SMA crosses above long-term EMA: Buy/Increase position
            log(f"Golden cross detected for {self.ticker}. Considering to go long.")
            allocation_dict[self.ticker] = 1  # Full allocation to this asset
        elif short_term_sma < long_term_ema:
            # If short-term SMA crosses below long-term EMA: Sell/Short position
            log(f"Death cross detected for {self.ticker}. Considering to exit or go short.")
            allocation_dict[self.ticker] = 0  # No allocation to this asset
        
        return TargetAllocation(allocation_dict)
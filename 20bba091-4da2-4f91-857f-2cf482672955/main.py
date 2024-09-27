from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the currency or asset you're trading.
        self.ticker = "EURUSD"  # Placeholder for the currency pair.
        self.rsi_period = 14  # Commonly used RSI period.
        self.rsi_threshold = 30  # RSI level indicating oversold conditions.
        self.break_count = 0  # To count the number of times RSI breaks the threshold.
        self.interval_count = 0  # To count intervals for resetting the break counter.
        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "15min"

    def run(self, data):
        # Initialize allocation with no position.
        allocation = 0
        
        # Retrieve RSI values for the ticker.
        rsi_values = RSI(self.ticker, data["ohlcv"], length=self.rsi_period)
        
        if len(rsi_values) > 3:  # Ensure there's enough data for analysis.
            # Check the last 3 RSI values to see if they broke the threshold from below.
            for rsi_value in rsi_values[-3:]:
                if rsi_value > self.rsi_threshold:
                    self.break_count += 1
                    break  # Assuming break from below once per interval counts once.
                    
            if self.break_count >= 3:  # Condition for trade trigger.
                log("Trading condition met, entering trade on next 5min uptrend.")
                allocation = 1  # Mock allocation for buy signal.
                self.break_count = 0  # Reset break counter after condition is met.
            else:
                log("Condition not met, holding position.")
                
            # Every 3 intervals of 15min equals 45min, potentially aligning with trading strategy timing.
            self.interval_count += 1
            if self.interval_count >= 3:
                self.interval_count = 0
                self.break_count = 0  # Reset break counts for fresh calculations.

        # Assuming only going long for simplicity. For actual strategy, consider exit or short conditions.
        return TargetAllocation({self.ticker: allocation})
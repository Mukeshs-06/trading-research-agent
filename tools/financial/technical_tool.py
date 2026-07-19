from langchain_core.tools import tool
import yfinance as yf
import pandas as pd
from core.logger import logger


@tool
def technical_analysis(ticker: str) -> dict:
    """
    Calculate technical indicators for a stock using historical price data.

    Calculates:
    - Current Price, SMA20, SMA50, EMA20, RSI (14), MACD, MACD Signal Line,
      Average Volume, Latest Volume, 6-month Support/Resistance swing levels, and Trend Direction.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")

        if df.empty:
            logger.warning(f"No historical data returned for {ticker}")
            return {"error": f"No historical data found for {ticker}."}

        close = df["Close"]
        high = df["High"] if "High" in df else close
        low = df["Low"] if "Low" in df else close
        volume = df["Volume"]

        # Simple Moving Averages
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()

        # Exponential Moving Average
        ema20 = close.ewm(span=20).mean()

        # Relative Strength Index (RSI)
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))

        # MACD (12, 26, 9)
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        current_p = float(close.iloc[-1])
        sma20_v = float(sma20.iloc[-1]) if not pd.isna(sma20.iloc[-1]) else current_p
        sma50_v = float(sma50.iloc[-1]) if not pd.isna(sma50.iloc[-1]) else current_p

        # Trend Determination & Evidence
        bullish_signals = 0
        bearish_signals = 0
        neutral_signals = 0

        if current_p > sma20_v:
            bullish_signals += 1
        else:
            bearish_signals += 1

        if sma20_v > sma50_v:
            bullish_signals += 1
        else:
            bearish_signals += 1

        latest_macd = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else 0.0
        latest_signal = float(signal.iloc[-1]) if not pd.isna(signal.iloc[-1]) else 0.0

        if latest_macd > latest_signal:
            bullish_signals += 1
        else:
            bearish_signals += 1

        latest_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0
        if 30 <= latest_rsi <= 70:
            neutral_signals += 1
        elif latest_rsi > 70:
            bearish_signals += 1 # Overbought
        else:
            bullish_signals += 1 # Oversold bounce potential

        if bullish_signals > bearish_signals:
            trend = "Bullish Momentum"
        elif bearish_signals > bullish_signals:
            trend = "Bearish Momentum"
        else:
            trend = "Neutral / Consolidation"

        # True 6-month Support (min low) and Resistance (max high)
        support = float(low.min())
        resistance = float(high.max())

        # Confidence Score calculation based on signal alignment
        total_signals = bullish_signals + bearish_signals + neutral_signals
        dominant = max(bullish_signals, bearish_signals)
        confidence_score = round((dominant / max(total_signals, 1)) * 100, 1)

        return {
            "ticker": ticker.upper(),
            "current_price": round(current_p, 2),
            "SMA20": round(sma20_v, 2),
            "SMA50": round(sma50_v, 2),
            "EMA20": round(float(ema20.iloc[-1]), 2),
            "RSI": round(latest_rsi, 2),
            "RSI_status": "Overbought (>70)" if latest_rsi > 70 else ("Oversold (<30)" if latest_rsi < 30 else "Neutral (30-70)"),
            "MACD": round(latest_macd, 2),
            "MACD_Signal": round(latest_signal, 2),
            "Average_Volume": int(volume.mean()),
            "Latest_Volume": int(volume.iloc[-1]),
            "Trend": trend,
            "Support_6M": round(support, 2),
            "Resistance_6M": round(resistance, 2),
            "Evidence": f"{bullish_signals} Bullish, {bearish_signals} Bearish, {neutral_signals} Neutral",
            "Confidence_Score": f"{confidence_score}%",
        }
    except Exception as e:
        logger.error(f"Technical analysis failed for {ticker}: {e}")
        return {
            "ticker": ticker.upper(),
            "error": f"Failed technical analysis: {str(e)}"
        }
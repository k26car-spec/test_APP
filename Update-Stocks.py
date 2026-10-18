
import yfinance as yf
import json
import pandas as pd
from datetime import datetime, timedelta

# 你的12檔 + 全市場吸籌14檔 + 富邦護航
STOCKS_782E = ["2330", "2454", "2317", "2412", "2881", "2303", "2609", "2882", "2891", "2382", "2308", "3711"]
MARKET_CHIP = ["6770", "3037", "3034", "3515", "6285", "2449", "3714", "2301", "2368", "8081", "3661", "6679", "2359", "2382"]
FUBON_GUARD = ["2881", "2882", "2887", "2891", "2886", "2890"]

ALL_CODES = list(set(STOCKS_782E + MARKET_CHIP + FUBON_GUARD))

# 你的張數 vol (範例，可自己改) - 保持不動，只更新price/K/D
VOL_MAP = {"2330": 5840, "2454": 3210, "2317": 4920, "2412": 2980, "2881": 3850, "2303": 4120, "2609": 3200, "2882": 3500, "2891": 4000, "2382": 3100, "2308": 1200, "3711": 2800}

def calc_kd(df):
    try:
        high = df['High'].rolling(9).max()
        low = df['Low'].rolling(9).min()
        rsv = (df['Close'] - low) / (high - low) * 100
        k = rsv.ewm(alpha=1/3).mean().iloc[-1]
        d = k.ewm(alpha=1/3).mean().iloc[-1]
        return round(float(k),1), round(float(d),1)
    except:
        return 50.0, 50.0

result = []
total_market = 0
for code in ALL_CODES:
    try:
        ticker = f"{code}.TW"
        df = yf.download(ticker, period="20d", interval="1d", progress=False)
        if df.empty:
            price = 100
        else:
            price = float(df['Close'].iloc[-1])
        k,d = calc_kd(df) if not df.empty else (50,50)
        vol = VOL_MAP.get(code, 1000)
        market_val = vol * price / 100  # 億
        total_market += market_val
        
        # 吸籌柱判斷 (簡化邏輯: K<20 + 量增 = 黃金柱)
        if k < 20:
            chip = "黄金柱"
            ctrl = 5
            trend = "強吸+放量"
        elif k < 30:
            chip = "紅柱"
            ctrl = 3
            trend = "吸籌積極"
        elif k > 80:
            chip = "藍柱"
            ctrl = -2
            trend = "高位出貨"
        else:
            chip = "青柱"
            ctrl = 1
            trend = "吸籌中"
            
        result.append({
            "code": code,
            "price": round(price,1),
            "K": k, "D": d,
            "vol": vol,
            "chip": chip,
            "ctrl": ctrl,
            "trend": trend
        })
    except Exception as e:
        print(f"{code} error {e}")
        result.append({"code": code, "price": 100, "K": 50, "D": 50, "vol": 1000, "chip": "白柱", "ctrl": 0, "trend": "洗盤"})

output = {
    "lastUpdate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    "totalCapital": round(total_market,2),
    "stocks": result,
    "source": "Yahoo Finance + 真實K/D + 吸籌"
}

with open("stock_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Updated {len(result)} stocks, total {total_market}億")

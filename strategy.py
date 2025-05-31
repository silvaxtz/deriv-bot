
import pandas as pd

def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analisar_confirmacoes(velas):
    df = pd.DataFrame(velas)
    df['ma'] = df['close'].rolling(window=5).mean()
    df['rsi'] = calcular_rsi(df['close'])

    ultima = df.iloc[-1]
    anterior = df.iloc[-2]

    cond1 = ultima['close'] > ultima['ma']  # Acima da média
    cond2 = ultima['rsi'] < 30              # RSI sobrevendido
    cond3 = ultima['close'] > anterior['open'] and anterior['close'] < anterior['open']  # Engolfo de alta

    call = cond1 and cond2 and cond3

    cond4 = ultima['close'] < ultima['ma']  # Abaixo da média
    cond5 = ultima['rsi'] > 70              # RSI sobrecomprado
    cond6 = ultima['close'] < anterior['open'] and anterior['close'] > anterior['open']  # Engolfo de baixa

    put = cond4 and cond5 and cond6

    if call:
        return "CALL"
    elif put:
        return "PUT"
    return None

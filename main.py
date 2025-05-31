
import requests
import time
from deriv_bot import DerivBot
from telegram_notify import enviar_telegram

def obter_ativos():
    ativos = []
    try:
        r = requests.get("https://api.deriv.com/api/contract_types")
        data = r.json()
        for key, val in data.get("contract_types", {}).items():
            ativos.extend(val)
        return list(set(ativos))
    except:
        return ["R_100", "WLDAUD", "BTCUSD"]

if __name__ == "__main__":
    enviar_telegram("🤖 Robô iniciado com todos os ativos.")
    ativos = obter_ativos()
    print("Ativos:", ativos)

    for ativo in ativos[:5]:  # Limite para 5 para testes
        try:
            bot = DerivBot(ativo)
            bot.iniciar()
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao iniciar bot para {ativo}: {e}")

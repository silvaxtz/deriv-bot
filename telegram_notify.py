
import requests

BOT_TOKEN = '7473874900:AAFvL95mIObMlaNpDWfbKNLMRpCJU3-vUcw'
CHAT_ID = '-4867702597'

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensagem}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro Telegram:", e)

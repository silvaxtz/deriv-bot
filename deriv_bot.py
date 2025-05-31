
import json
import websocket
import threading
import time
from strategy import analisar_confirmacoes
from telegram_notify import enviar_telegram

API_TOKEN = 'KYP2DIKaRJJzo8Y'
DURATION = 1

class DerivBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.placar = {"acertos": 0, "erros": 0}
        self.ws = websocket.WebSocketApp(
            "wss://ws.derivws.com/websockets/v3?app_id=1089",
            on_open=self.on_open,
            on_message=self.on_message
        )
        self.valor_entrada = 1.0  # valor inicial
        self.proximo_valor = 1.0  # valor da próxima entrada (soros)

    def iniciar(self):
        t = threading.Thread(target=self.ws.run_forever)
        t.start()

    def on_open(self, ws):
        ws.send(json.dumps({"authorize": API_TOKEN}))

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get("msg_type") == "authorize":
            ws.send(json.dumps({
                "ticks_history": self.symbol,
                "adjust_start_time": 1,
                "count": 100,
                "end": "latest",
                "style": "candles",
                "granularity": 60
            }))
        elif data.get("msg_type") == "candles":
            candles = data["candles"]
            for c in candles:
                c["open"] = float(c["open"])
                c["close"] = float(c["close"])
            direcao = analisar_confirmacoes(candles)
            if direcao:
                self.enviar_ordem(direcao)
        elif data.get("msg_type") == "buy":
            enviar_telegram(f"🎯 {self.symbol}: Ordem enviada ({data['buy']['contract_type']}) com ${self.proximo_valor:.2f}")
        elif data.get("msg_type") == "proposal_open_contract":
            if data["proposal_open_contract"]["is_sold"]:
                resultado = "win" if data["proposal_open_contract"]["profit"] > 0 else "loss"
                self.registrar_resultado(resultado, data["proposal_open_contract"]["profit"])

    def enviar_ordem(self, direcao):
        contrato = {
            "buy": 1,
            "price": round(self.proximo_valor, 2),
            "parameters": {
                "amount": round(self.proximo_valor, 2),
                "basis": "stake",
                "contract_type": direcao,
                "currency": "USD",
                "duration": DURATION,
                "duration_unit": "m",
                "symbol": self.symbol
            }
        }
        self.ws.send(json.dumps(contrato))

    def registrar_resultado(self, resultado, lucro):
        if resultado == "win":
            self.placar["acertos"] += 1
            self.proximo_valor = 1 + lucro  # soros nível 1
        else:
            self.placar["erros"] += 1
            self.proximo_valor = self.valor_entrada  # reset soros

        enviar_telegram(f"{self.symbol} ▶️ ✅ {self.placar['acertos']} | ❌ {self.placar['erros']} | Próx: ${self.proximo_valor:.2f}")

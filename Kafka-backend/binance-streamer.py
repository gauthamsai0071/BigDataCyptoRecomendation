import websocket
import datetime
import kafkawriter
import sys

def on_message(ws, message):
    print()
    print(str(datetime.datetime.now()) + ": ")
    print(message)
    kafkawriter.log_kafka(symbol, message)

def trade_message(ws, message):
    print()
    print(str(datetime.datetime.now()) + ": ")
    print(message)
    kafkawriter.log_kafka_trade(symbol, message)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamKline(currency, interval):
    websocket.enableTrace(False)
    socket = f'wss://stream.binance.us:9443/ws/{currency}@kline_{interval}'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

def streamTrade(currency):
    websocket.enableTrace(False)
    socket = f'wss://stream.binance.us:9443/ws/{currency}@trade'
    ws = websocket.WebSocketApp(socket,
                                on_message=trade_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

kafkawriter.init_kafkawriter()

if __name__ == "__main__":
    symbol = sys.argv[1]
    interval = sys.argv[2]
    streamtades = sys.argv[3]

    print("symbol: " + symbol)
    print("interval: " + interval)
    print("streamtades: " +streamtades)
    if(streamtades == "1"):
        streamTrade(symbol)
    else:
        streamKline(symbol, interval)

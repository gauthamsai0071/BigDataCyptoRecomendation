STEP 1: GET KAFKA
Download the latest Kafka release and extract it:

$ tar -xzf kafka_2.13-3.4.0.tgz
$ cd kafka_2.13-3.4.0

STEP 2: START THE KAFKA ENVIRONMENT
NOTE: Your local environment must have Java 8+ installed.

Apache Kafka can be started using ZooKeeper or KRaft. To get started with either configuration follow one the sections below but not both.

Kafka with ZooKeeper
Run the following commands in order to start all services in the correct order:

# Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties
Open another terminal session and run:

# Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties
Once all services have successfully launched, you will have a basic Kafka environment running and ready to use.

STEP 3: CREATE A TOPIC TO STORE YOUR EVENTS
Kafka is a distributed event streaming platform that lets you read, write, store, and process events (also called records or messages in the documentation) across many machines.

Example events are payment transactions, geolocation updates from mobile phones, shipping orders, sensor measurements from IoT devices or medical equipment, and much more. These events are organized and stored in topics. Very simplified, a topic is similar to a folder in a filesystem, and the events are the files in that folder.

So before you can write your first events, you must create a topic. Open another terminal session and run:

$ bin/kafka-topics.sh --create --topic solusd --bootstrap-server localhost:9092
All of Kafka's command line tools have additional options: run the kafka-topics.sh command without any arguments to display usage information. For example, it can also show you details such as the partition count of the new topic:

$ bin/kafka-topics.sh --describe --topic solusd --bootstrap-server localhost:9092
Topic: quickstart-events        TopicId: NPmZHyhbR9y00wMglMH2sg PartitionCount: 1       ReplicationFactor: 1	Configs:
    Topic: quickstart-events Partition: 0    Leader: 0   Replicas: 0 Isr: 0


STEP 4: Stream trade data and K-line data from Binance websockets

Binance Endpoints:

# Web Socket Streams for Binance (2022-11-28)
# General WSS information
* The base endpoint is: **wss://stream.binance.us:9443**
* Streams can be accessed either in a single raw stream or in a combined stream
* Raw streams are accessed at **/ws/\<streamName\>**
* Combined streams are accessed at **/stream?streams=\<streamName1\>/\<streamName2\>/\<streamName3\>**
* Combined stream events are wrapped as follows: **{"stream":"\<streamName\>","data":\<rawPayload\>}**
* All symbols for streams are **lowercase**
* A single connection to **stream.binance.us** is only valid for 24 hours; expect to be disconnected at the 24 hour mark
* The websocket server will send a `ping frame` every 3 minutes. If the websocket server does not receive a `pong frame` back from the connection within a 10 minute period, the connection will be disconnected. Unsolicited `pong frames` are allowed.

## Trade Streams
The Trade Streams push raw trade information; each trade has a unique buyer and seller.

**Stream Name:** \<symbol\>@trade
eg \btcusd@trade

**Update Speed:** Real-time

**Payload:**
```javascript
{
  "e": "trade",          // Event type
  "E": 1672515782136,    // Event time
  "s": "BNBBTC",         // Symbol
  "t": 12345,            // Trade ID
  "p": "0.001",          // Price
  "q": "100",            // Quantity
  "b": 88,               // Buyer order ID
  "a": 50,               // Seller order ID
  "T": 1672515782136,    // Trade time
  "m": true,             // Is the buyer the market maker?
  "M": true              // Ignore
}
```

## Kline/Candlestick Streams
The Kline/Candlestick Stream push updates to the current klines/candlestick every second.

**Kline/Candlestick chart intervals:**

s-> seconds; m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

* 1s
* 1m
* 3m
* 5m
* 15m
* 30m
* 1h
* 2h
* 4h
* 6h
* 8h
* 12h
* 1d
* 3d
* 1w
* 1M

**Stream Name:** \<symbol\>@kline_\<interval\>

**Update Speed:** 1000ms for `1s`, 2000ms for the other intervals

**Payload:**
```javascript
{
  "e": "kline",         // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",        // Symbol
  "k": {
    "t": 1672515780000, // Kline start time
    "T": 1672515839999, // Kline close time
    "s": "BNBBTC",      // Symbol
    "i": "1m",          // Interval
    "f": 100,           // First trade ID
    "L": 200,           // Last trade ID
    "o": "0.0010",      // Open price
    "c": "0.0020",      // Close price
    "h": "0.0025",      // High price
    "l": "0.0015",      // Low price
    "v": "1000",        // Base asset volume
    "n": 100,           // Number of trades
    "x": false,         // Is this kline closed?
    "q": "1.0000",      // Quote asset volume
    "V": "500",         // Taker buy base asset volume
    "Q": "0.500",       // Taker buy quote asset volume
    "B": "123456"       // Ignore
  }
}
```


## binance-streamer.py
Install the required libraries
pip install kafka-python
pip install websocket

The function of this program is read from the binance streams related to the particular crypto and the write those binance streams to a kafka topic.
The producer in this case for the kafka streaming is the websocket stream from binance.
The consumer in this case for the kafka streaming is MongoDB
Command to run it: python3 binance-streamer.py solusd 1m 1

Arguments: 
    Argument1: symbol: The crypto currency we want to stream
    Argument2: interval: The interval at which we want k-line candlesticks
    Argument3: streamtades: If 1 then it streams trades related to the crypto we specified, if not it reads k-line data from the binance stream


## kafkawriter.py
kafkawriter.py is a Python script that reads data from a WebSocket connection and writes it to a corresponding Kafka topic. It accepts the symbol and message as arguments from another Python program.

Requirements
Python 3.x
kafka-python library (install using pip install kafka-python)
websocket library (install using pip install websocket)

## Mongowriter.py

`mongowriter.py` is a Python program that reads messages from a Kafka topic and writes incremental messages to MongoDB based on the specified database, collection, group, and trade configuration.
Mongo DB is hosted on Atlas
pip install pymongo
Arguments: 
    Argument1: database: The crypto currency we want to stream
    Argument2: collection: The interval at which we want k-line candlesticks
    Argument3: group:
    Argument4: trade: if 1 then it streams trades related to the crypto we specified, if not it reads k-line data from the binance stream




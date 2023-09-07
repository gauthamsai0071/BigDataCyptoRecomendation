#Extract Kafka Jar
tar -xzf kafka_2.13-3.4.0.tgz

#Change the folder to the extracted jar
cd kafka_2.13-3.4.0

#Start Apache Zookeeper. Zookeeper helps manage Kafka and other products in Apache Big Data collection
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties

#Start Kafka server as a local server on the system
bin/kafka-server-start.sh -daemon config/server.properties
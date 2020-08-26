echo "The status of the connectors:\n\n"

curl -s "http://localhost:8083/connectors?expand=info&expand=status" | \
           jq '. | to_entries[] | [ .value.info.type, .key, .value.status.connector.state,.value.status.tasks[].state,.value.info.config."connector.class"]|join(":|:")' | \
           column -s : -t| sed 's/\"//g'| sort

echo "\n\nVersion of MongoDB Connector for Apache Kafka installed:\n"
curl --silent http://localhost:8083/connector-plugins | jq -c '.[] | select( .class == "com.mongodb.kafka.connect.MongoSourceConnector" or .class == "com.mongodb.kafka.connect.MongoSinkConnector" )'

echo "\nWSchemas in Schema Registry:\n\n"
curl --silent -X GET http://localhost:8081/subjects | jq

echo "\n\nAvro Schema from MongoDB : stockdata.Stocks.StockData-value"
curl --silent -X GET http://localhost:8081/subjects/stockdata.Stocks.StockData-value/versions/1 | jq

echo "\n\nAvro Schema from MySQL"
curl --silent -X GET http://localhost:8081/subjects/mysqlstock.Stocks.StockData-value/versions/1 | jq

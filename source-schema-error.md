
# Defined schema

curl -X POST -H "Content-Type: application/json" --data '
  {"name": "mongo-source-stockdata",
   "config": {
     "tasks.max":"1",
     "connector.class":"com.mongodb.kafka.connect.MongoSourceConnector",
     "output.json.formatter":"com.mongodb.kafka.connect.source.json.formatter.SimplifiedJson",
     "output.format.value":"schema",
     "output.schema.value":"{\"name\":\"MongoExchangeSchema\",\"type\":\"record\",\"namespace\":\"com.mongoexchange.avro\",\"fields\":[ {\"name\": \"_id\",\"type\": \"string\"},{\"name\": \"company_symbol\",\"type\": \"string\"},{\"name\": \"company_name\",\"type\": \"string\"},{ \"name\": \"price\",\"type\": \"float\"},{\"name\": \"tx_time\",\"type\": \"string\"}]}",
     "output.format.key":"json",
     "key.converter":"org.apache.kafka.connect.storage.StringConverter",
     "value.converter":"io.confluent.connect.avro.AvroConverter",
     "value.converter.schema.registry.url":"http://schema-registry:8081",
     "transforms": "InsertField",
     "transforms.InsertField.type": "org.apache.kafka.connect.transforms.InsertField$Value",
     "transforms.InsertField.static.field": "Exchange",
     "transforms.InsertField.static.value": "MongoDB",
     "publish.full.document.only": true,
     "connection.uri":"mongodb://mongo1:27017,mongo2:27017,mongo3:27017",
     "topic.prefix":"stockdata",
     "database":"Stocks",
     "collection":"StockDataError",
     "errors.tolerance":true
}}' http://localhost:8083/connectors -w "\n"

# Infered schema

curl -X POST -H "Content-Type: application/json" --data '
  {"name": "mongo-source-stockdata",
   "config": {
     "tasks.max":"1",
     "connector.class":"com.mongodb.kafka.connect.MongoSourceConnector",
     "output.json.formatter":"com.mongodb.kafka.connect.source.json.formatter.SimplifiedJson",
     "output.format.value":"schema",
     "output.schema.infer.value":true,
     "output.format.key":"json",
     "key.converter":"org.apache.kafka.connect.storage.StringConverter",
     "value.converter":"io.confluent.connect.avro.AvroConverter",
     "value.converter.schema.registry.url":"http://schema-registry:8081",
     "publish.full.document.only": true,
     "connection.uri":"mongodb://mongo1:27017,mongo2:27017,mongo3:27017",
     "topic.prefix":"stockdata",
     "database":"Stocks",
     "collection":"StockDataError",
     "errors.tolerance":"all"
}}' http://localhost:8083/connectors -w "\n"


# MongoDB Connector for Apache Kafka V1.3 example - Stock Exchange example

This demo generates fake stock data and populates two databases - MySQL and MongoDB.  Data flows from these databases to Kafka topics via their respetive connectors - Debezium MySQL and MongoDB Connector for Apache Kafka.  Data from both topics are then sinked to a MongoDB cluster in MongoDB Atlas using the MongoDB Connector for Apache Kafka as a sink.  

This demo highlights MongoDB Connection for Apache Kafka version 1.3 features including:
- Schema support in source connector

This README will cover how to get the environment up and running, for a tour of the features using this demo environment read the <B>TODO: BLOG POST</B> and `demo-script.txt` file.

Note: Until version 1.3 is formally released this repo will contain the snapshot build of 1.3 of the connector.  It is not a production ready build.

## Requirements
  - Docker 18.09+
  - Docker compose 1.24+
  - [jq](https://stedolan.github.io/jq/)
  - [kafkacat](https://github.com/edenhill/kafkacat)

## Running the demo
### 1. Download/Clone the docker files from the GitHub repository

[https://github.com/RWaltersMA/kafka1.3.git](https://github.com/RWaltersMA/kafka1.3.git)

### 2. Build the demo images

Run the following script from the command shell:

`Build-images.sh`

Note: Make sure you are in the same directory as the build-images script file.  Also, you may have to add execute permission via a `chmod +x build-images.sh` to execute the script.

This shell script will build the following images:

Image Name | Description
--------------- | -----------------
<B>mysqlimg</B> | Imagine of MySQL pre-configured with authentication
<B>stockgenmongo</B> | Runs Python app to create data and insert into local MongoDB cluster
<B>stockgenmysql</B> | Runs Python app to create data and insert into local MySQL Server
<B>stockportal</B> | Hosts webpage on localhost:8080 that shows the security symbols generated by the python apps

You can confirm these four images were created by issuing a `docker images` command.

### 3. Copy the Atlas Connection String

If you do not have a MongoDB Atlas cluster, [follow these instructions](https://docs.atlas.mongodb.com/getting-started/).

If you have not created a database user for the Kafka Connector:

Select, “Database Access” from the Atlas menu and click the “Add new User” button.  

Provide a username and password and select, “Read and write to any database”.  Remember the password.

If your docker host is not whitelisted in Atlas:
Click, “Network Access” from the Atlas menu and click, “Add IP Address”.  Here you can add your current IP address or any IP Address or block of addresses in CIDR format.  Note: If you do not know or can not obtain the IP address of the docker host you can add, “0.0.0.0” as an entry which will allow connections from anywhere on the internet.  This is not a recommended configuration.

To copy the connection string select the “CONNECT” button on your Atlas cluster then choose “Connect your application”.  Click the Copy button to copy the connection string to the clipboard.</p>

The connection string looks something like: 
<I><pre>mongodb+srv://USERNAME:PASSWORD@xxxxx.yyyyy.mongodb.net/test</pre></I>

Atlas does not put your actual password in the connection string.  You will need to replace the PASSWORD placeholder with your actual password in the next step where you provide this connection string as a parameter.

### 4. Execute the START-DEMO.SH script passing Atlas Connection String

The demo is now ready to go just issue a `sh start-demo.sh "<<paste in your Atlas Connection String here>>"` and the script will start the docker containers and configure the connectors.

## Running the Demo

Once the docker images and containers are built in steps 1-3, you can spin up this environment anytime by simply executing the `sh start-demo.sh "<<paste in your Atlas Connection String here>>"`

### 1. View the generated stock entities 

Open a web browser on your docker host and point to http://localhost:8080

The demo will randomly generate 10 securities, 5 for MySQL and 5 for MongoDB respectively.  This web page simply connects to MySQL and MongoDB and show the names of the stocks that will be used within the current iteration of the demo.  This piece is not critical to the demo, it just makes it much easier than logging in and performing SELECT/find queries.  To do fun things with the data you may want to know the security names created by the generators.

### 2. View the topic messages

Stockgenmongo and Stockgenmysql containers are running python apps that are pushing stock transactions into their respective databases.  Messages in <I>mysqlstock.Stocks.StockData</I> topic are using the Debezium MySQL connector.  Messages in the <I>stockdata.Stocks.StockData</I> topic came from the MongoDB Connector for Apache Kafka.  Messages present in these topics validates that our connectors are set up and working.

You can view the messages in these Kafka topics using the [Kafkacat](https://github.com/edenhill/kafkacat) tool.  This demo leverages the landoop kafka topic web UI and this can be found running on http://localhost:8000

![Landoop Kafka Topic](readme-images/LandoopUI.png)

### 3. View the combined data in MongoDB Atlas

The MongoDB Connector for Apache Kafka is configured as a sink connector and writes data to MongoDB Atlas.  Data is written to the StockData collection in the Stocks database.  Click on "Collections" tab in your MongoDB Atlas portal to view the StockData collection. These data are from both the MySQL and MongoDB databases.  There is an added field called Exchange that describes the database origin of the data.

![Atlas](readme-images/atlas.png)

## Something hit the fan and I dont know what to do - Troubleshooting

### Check the logs of the docker containers

`doocker ps`, get the container ID then `docker logs CONTAINERID`

### Doublecheck that you replaced the word PASSWORD with your actual password in the connection string to Atlas

### Use the status.h script file to dump useful info

There is a script file called, `status.h` running this will show you the version of the MongoDB connector installed in Kafka Connect, the status of the connectors, and other useful information.

![Status](readme-images/status.png)

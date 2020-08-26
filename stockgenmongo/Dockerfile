FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY *.txt ./

CMD [ "python", "./realtime-mongo.py", "-s","5", "-c", "mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0" ]

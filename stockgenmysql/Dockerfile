FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY *.txt ./

CMD [ "python", "./realtime-sql.py", "-c", "mysqlstock", "-s","5" ]

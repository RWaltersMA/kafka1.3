FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

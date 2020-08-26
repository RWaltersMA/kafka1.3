FROM mysql

ENV MYSQL_ROOT_PASSWORD=pass@word1

COPY setup.sql /docker-entrypoint-initdb.d/

RUN echo "[mysqld]" >> /etc/my.cnf
RUN echo "bind-address=0.0.0.0" >> /etc/my.cnf
RUN echo "server-id=223344" >> /etc/my.cnf
RUN echo "log_bin=mysql-bin" >> /etc/my.cnf
RUN echo "binlog_format=row" >> /etc/my.cnf
RUN echo "binlog_row_image=full" >> /etc/my.cnf
RUN echo "expire_logs_days=10" >> /etc/my.cnf

FROM mysql:8.0.32

# Copy the SQL scripts to the Docker image
COPY ./docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

# Set the MYSQL_ROOT_PASSWORD environment variable
ENV MYSQL_ROOT_PASSWORD=root_bot_buster

EXPOSE 3306

# Use the MySQL Docker entrypoint script, which will import the SQL scripts
CMD ["mysqld", "--init-file", "/docker-entrypoint-initdb.d/init.sql"]
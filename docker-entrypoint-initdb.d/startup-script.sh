#!/bin/bash
for script in /docker-entrypoint-initdb.d/*.sql; do
  mysql -u root -p"${MYSQL_ROOT_PASSWORD}" < "${script}"
done
exec mysqld
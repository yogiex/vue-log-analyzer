#!/bin/bash
set -a
source "$(dirname "$0")/.env"
set +a

min=$(date +%Y-%m-%d-%T)
fullpath=/var/lib/mysql-files/$min

mysql -u root -padmin@123 moodle < ../query-sql/log.sql
mysql -u root -padmin@123 moodle < ../query-sql/step.sql
mysql -u root -padmin@123 moodle < ../query-sql/attempt.sql

mkdir $fullpath
mv /var/lib/mysql-files/*.csv $fullpath 
echo $fullpath
sleep 5
sshpass -p "$PASSWORD" rsync -a --remove-source-files -e "ssh -p $PORT " /var/lib/mysql-files/$min "$REMOTE_USER"@"$REMOTE_HOST:~/backup-sql

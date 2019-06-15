#!/bin/sh
cd /var/www/html
service apache2 stop
service apache2 start
service mysql start
mysqladmin -uroot -proot password yeecent
mysql -uroot -pyeecent -e "source /var/www/html/xxxadmin.sql"
python new.py 15
/bin/bash
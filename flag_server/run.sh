#!/bin/sh
cd /var/www/html
service apache2 stop
service apache2 start
service mysql start
python new.py 15
/bin/bash
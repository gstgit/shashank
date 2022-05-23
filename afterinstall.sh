#!/bin/bash

cd /home/ubuntu
sudo apt-get update
sudo apt-get -y install python3-pip
sudo apt install python3-pip python3-dev nginx -Y
sudo pip3 install virtualenv
sudo virtualenv env 
source env/bin/activate
pip install django gunicorn
sudo pip install django gunicorn
cd rare_window_backend
sudo pip3 install -r requirements.txt
pip3 install -r requirements.txt
sudo apt-get install mysql-server-Y
sudo apt-get install libmysqlclient -y
deactivate
sudo apt-get install mysql-server-Y
sudo apt-get install libmysqlclient -y
pip install mysqlclient
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py collectstatic -yes
sudo ufw allow 80
sudo chmod -R 777 *
sudo mv /home/ubuntu/gunicorn.socket  /etc/systemd/system/ 
sudo mv /home/ubuntu/gunicorn.service  /etc/systemd/system/
cd  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn.socket
sudo systemctl restart gunicorn
sudo mv /home/ubuntu/app-site /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/app-site /etc/nginx/sites-enabled/
cd /etc/nginx/sites-available/
sudo rm -r default 
cd /etc/nginx/sites-enabled/
sudo rm -r default 
sudo systemctl restart nginx










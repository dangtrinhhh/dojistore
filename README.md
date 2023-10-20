# dojistore
My ecomerce website using Django, HTML, CSS, JavaScript

# Connect instance:
go to SSH client tab in EC2 instance

chmod 400 testing.pem

Example:
ssh -i "testing.pem" ubuntu@ec2-52-32-19-213.us-west-2.compute.amazonaws.com

sudo ufw app list

sudo ufw allow OpenSSH

sudo ufw enable

sudo ufw status

sudo apt update

sudo apt install python3-pip python3-dev libpq-dev nginx curl virtualenv

git clone YourRepo

cd YourProject

virtualenv venv 

source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations, migrate, collectstatic

sudo ufw allow 8000 

python manage.py runserver 0.0.0.0:8000

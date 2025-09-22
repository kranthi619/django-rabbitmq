# on your workstation
ssh -i ~/.ssh/mykey.pem ubuntu@<ec2-ip>


# on EC2
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
sudo apt install rabbitmq-server -y
sudo systemctl enable rabbitmq-server --now
# (optional) enable RabbitMQ management plugin
sudo rabbitmq-plugins enable rabbitmq_management
# open firewall (if using ufw)
sudo ufw allow OpenSSH
sudo ufw allow 5672
sudo ufw allow 15672
sudo ufw allow 80
sudo ufw --force enable


# clone your repo
[git clone https://github.com/<you>/django-rabbitmq-microservices.git]
https://github.com/kranthi619/django-rabbitmq
cd django-rabbitmq-microservices


# create virtualenv (for each service you can create venvs or one global venv)
python3 -m venv venv
source venv/bin/activate
pip install -r re

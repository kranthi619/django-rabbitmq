import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

RABBITMQ_HOST = getattr(settings, 'RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = getattr(settings, 'RABBITMQ_PORT', 5672)
EXCHANGE_NAME = 'user_exchange'
ROUTING_KEY = 'user.created.key'

def publish_message(user_data):
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()
# direct exchange (explicit)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)
channel.basic_publish(
exchange=EXCHANGE_NAME,
routing_key=ROUTING_KEY,
body=json.dumps(user_data),
properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
)
connection.close()

@api_view(['POST'])
def register_user(request):
username = request.data.get('username')
password = request.data.get('password')
email = request.data.get('email')
first_name = request.data.get('first_name', '')
last_name = request.data.get('last_name', '')

if not username or not password or not email:
return Response({'error': 'username, password and email required.'}, status=status.HTTP_400_BAD_REQUEST)

if User.objects.filter(username=username).exists():
return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

user = User.objects.create_user(username=username, password=password, email=email,
first_name=first_name, last_name=last_name)

user_data = {
'id': user.id,
'username': user.username,
'email': user.email,
'first_name': user.first_name,
'last_name': user.last_name
}

try:
publish_message(user_data)
except Exception as e:
# If publish fails, you can still return success but also log / retry later
print('Failed to publish message to RabbitMQ:', e)

return Response({'message': 'User registered successfully', 'user': user_data}, status=status.HTTP_201_CREATED)

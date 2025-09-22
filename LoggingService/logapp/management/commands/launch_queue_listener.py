import json
import pika
import threading
import time
from django.core.management.base import BaseCommand
from django.conf import settings


RABBITMQ_HOST = getattr(settings, 'RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = getattr(settings, 'RABBITMQ_PORT', 5672)
EXCHANGE_NAME = 'user_exchange'
ROUTING_KEY = 'user.created.key'
QUEUE_NAME = 'logging_queue'




def log_user(user_data):
# This simply prints; in prod, write to a logging system or centralized store
print(f"[LoggingService] New user created: {user_data.get('username')} (id={user_data.get('id')})")




def callback(ch, method, properties, body):
try:
user_data = json.loads(body)
except Exception:
print('[LoggingService] Failed to decode message')
return


log_user(user_data)




class ListenerThread(threading.Thread):
def run(self):
while True:
try:
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)


print('[LoggingService] Waiting for messages...')
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=lambda ch, method, props, body: (callback(ch, method, props, body), ch.basic_ack(method.delivery_tag)), auto_ack=False)
channel.start_consuming()
except Exception as e:
print('[LoggingService] Listener crashed:', e)
time.sleep(5)




class Command(BaseCommand):
help = 'Launch queue listener'


def handle(self, *args, **options):
ListenerThread().start()

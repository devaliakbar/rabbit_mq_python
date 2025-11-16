import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
channel.confirm_delivery()

message = "1"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")


message = "2"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")


message = "3"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")


message = "4"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")
connection.close()

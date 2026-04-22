import pika
import time


def get_connection(retries=20, delay=3):
    params = pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        credentials=pika.PlainCredentials("guest", "guest")
    )

    for attempt in range(retries):
        try:
            return pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready, retry {attempt + 1}/{retries}")
            time.sleep(delay)

    raise Exception("Could not connect to RabbitMQ")
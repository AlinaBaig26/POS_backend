import json
import uuid
import pika
from .rabbitmq import get_connection
import time

class RpcClient:
    def __init__(self):
        self.connection = get_connection()
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.response = None
        self.correlation_id = None

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.correlation_id:
            self.response = body

    def call(self, queue_name, payload, timeout=10):
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        self.channel.queue_declare(queue=queue_name, durable=True)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
                content_type="application/json",
                delivery_mode=2
            ),
            body=json.dumps(payload)
        )

        start = time.time()
        while self.response is None:
            self.connection.process_data_events(time_limit=1)
            if time.time() - start > timeout:
                raise TimeoutError(f"RPC timeout waiting for response from {queue_name}")

        return json.loads(self.response.decode())

    def close(self):
        self.connection.close()
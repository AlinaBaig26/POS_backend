import json
import pika
from .rabbitmq import get_connection
from customer_app.customer_api.customer.service import CustomerService

service = CustomerService()

def get_customer_by_name(name):
    customer = service.getCustomerByName(name)

    if not customer:
        return {"error": f"Customer with name {name} not found."}

    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone
    }


def handle_request(payload):
    action = payload.get("action")

    if action == "get_customer_by_name":
        name = payload.get("name")
        return get_customer_by_name(name)

    return {"error": f"Unknown action: {action}"}


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="customer.rpc.queue", durable=True)
    channel.basic_qos(prefetch_count=1)

    def on_request(ch, method, props, body):
        try:
            payload = json.loads(body.decode())
            response = handle_request(payload)
        except Exception as e:
            response = {"error": str(e)}

        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id,
                content_type="application/json"
            ),
            body=json.dumps(response)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue="customer.rpc.queue",
        on_message_callback=on_request
    )

    print("Waiting for customer RPC requests...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
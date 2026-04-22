import json
import pika
from .rabbitmq import get_connection
from supplier_app.supplier_api.supplier.service import SupplierService

service = SupplierService()

def get_supplier_by_name(name):
    supplier = service.getSupplierByName(name)

    if not supplier:
        return {"error": f"Supplier with name {name} not found."}
    
    return {
        "id": supplier.id,
        "name": supplier.name,
        "phone": supplier.phone
    }


def handle_request(payload):
    action = payload.get("action")

    if action == "get_supplier_by_name":
        name = payload.get("name")
        return get_supplier_by_name(name)

    return {"error": f"Unknown action: {action}"}


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="supplier.rpc.queue", durable=True)
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
        queue="supplier.rpc.queue",
        on_message_callback=on_request
    )

    print("Waiting for supplier RPC requests...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
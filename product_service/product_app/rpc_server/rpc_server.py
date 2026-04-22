import json
import pika
from .rabbitmq import get_connection
from product_app.product_api.product.service import ProductService

service = ProductService()

# Replace this with your actual repository/service import
# from product_app.product_api.products.service import ProductService


def get_product_by_sku(sku):
    # Demo response
    product = service.getProductBySku(sku)
    if not product:
        return {"error": f"Product with sku {sku} not found."}

    return {"id": product.id,
            "name": product.name,
            "description": product.description,
            "sku": product.sku,
            "price": product.price,
            "cost_price": product.cost_price}


def handle_request(payload):
    action = payload.get("action")

    if action == "get_product_by_sku":
        sku = payload.get("sku")
        return get_product_by_sku(sku)

    return {"error": f"Unknown action: {action}"}


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="product.rpc.queue", durable=True)
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
        queue="product.rpc.queue",
        on_message_callback=on_request
    )

    print("Waiting for product RPC requests...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
import asyncio
from time import sleep

import ujson as json
from aio_pika import Message, connect
from src.tools.rabbit_client import RabbitClient
from src.config.setup import settings


async def send_test_message():
    rabbit_url = "amqp://admin:rabbit@localhost:5672/vhost"  # Ensure this is correctly set
    queue_name = "mission"  # The queue your service is consuming from

    connection = await connect(rabbit_url)
    channel = await connection.channel()

    for i in range(2):
        message = {
            "body": {
                "content": "Hello, RabbitMQ!",
                "type": "Hello, RabbitMQ!",
                "data": {
                    "customer_name": f"Customer {i}",
                    "amount": round(100 + i * 10.5, 2),
                    "status": "pending",
                    "issued_at": "2025-03-29T12:00:00Z"
                },
            },
            "metadata": {
                "timestamp": "2025-03-29T12:00:00Z",
                "sender": "test",
                "version": "0.0.1",
            },
            "operation": "create_invoice"
        }

        message_body = Message(
            content_type="application/json",
            body=json.dumps(message, ensure_ascii=False).encode(),
        )
        await channel.default_exchange.publish(
            message_body, routing_key=queue_name
        )
        sleep(5)

    print(f"[x] Sent: {message}")
    await connection.close()


if __name__ == "__main__":
    asyncio.run(send_test_message())

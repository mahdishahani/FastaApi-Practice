import asyncio
from time import sleep

import ujson as json
from aio_pika import Message, connect
from src.tools.rabbit_client import RabbitClient  # Adjust the import path as needed
from src.config.setup import settings  # Ensure you have your RabbitMQ settings


async def send_test_message():
    rabbit_url = "amqp://admin:rabbit@localhost:5672/vhost"  # Ensure this is correctly set
    queue_name = "mission"  # The queue your service is consuming from

    connection = await connect(rabbit_url)
    channel = await connection.channel()

    for i in range(100):
        message = {
            "metadata": {"id": "12345", "timestamp": "2025-02-25T12:00:00Z"},
            "data": f"Test message for RabbitMQ -  - -- - -  - {i}",
            "operation": "add_invoice"
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

import asyncio
import aio_pika


async def main():
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        channel = await connection.channel()

        await channel.declare_queue("task_queue", durable=True)

        for i in range(1, 5):
            message = aio_pika.Message(
                body=str(i).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await channel.default_exchange.publish(
                message,
                routing_key="task_queue",
            )
            print(f" [x] Sent {i}")


if __name__ == "__main__":
    asyncio.run(main())

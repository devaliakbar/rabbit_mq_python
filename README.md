# RabbitMQ Python Example

## Work Queues

### Sender

```python
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
```

### Receiver

```python
import asyncio
import aio_pika


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        print(f" [x] Received {body}")
        await asyncio.sleep(8)
        print(f" [x] Done {body}")


async def main():
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=2)

        queue = await channel.declare_queue("task_queue", durable=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
```

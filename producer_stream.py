import asyncio
import time
from argparse import ArgumentParser

from rstream import Producer, AMQPMessage, SuperStreamProducer
from rstream.amqp import encode_payload

parser = ArgumentParser(description="")
parser.add_argument("--stream", type=str)
parser.add_argument("--message", type=str)
args = parser.parse_args()



STREAM = args.stream
STREAM_RETENTION = 100000
MESSAGES = 1


async def publish():
    async with Producer("localhost", username="user", password="password") as producer:
        # create a stream if it doesn't already exist
        await producer.create_stream(STREAM, exists_ok=True, arguments={
        "MaxLengthBytes": STREAM_RETENTION,
        "MaxAge": "5s"
    })

        # sending a million of messages in binary format
        # note that this is not compatible with other clients (e.g. Java,.NET)
        # since they expect messages in AMQP 1.0
        start_time = time.perf_counter()

        for i in range(MESSAGES):
            # send is asynchronous
            await producer.send(stream=STREAM, message=bytes(args.message, encoding="utf-8"))

        end_time = time.perf_counter()
        print(f"Sent {MESSAGES} messages in {end_time - start_time:0.4f} seconds")


asyncio.run(publish())
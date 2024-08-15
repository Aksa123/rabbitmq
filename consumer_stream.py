import asyncio
import signal
from argparse import ArgumentParser

from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    ConsumerOffsetSpecification,
    OffsetType,
    amqp_decoder
)

parser = ArgumentParser()
parser.add_argument("--stream", type=str)
parser.add_argument("--name", type=str)
parser.add_argument("--single", type=bool, default=False)
parser.add_argument("--offset", default=0)
args = parser.parse_args()


STREAM = args.stream
STREAM_RETENTION = 100000

# offset_spec = ConsumerOffsetSpecification(OffsetType.OFFSET, args.offset) if args.offset > 0 else ConsumerOffsetSpecification(OffsetType.NEXT, None)
offset_spec = None
if type(args.offset) == int:
    offset_spec = ConsumerOffsetSpecification(OffsetType.OFFSET, args.offset)
elif type(args.offset) == str:
    if args.offset == "first":
        offset_spec = ConsumerOffsetSpecification(OffsetType.FIRST, None)
    elif args.offset == "last":
        offset_spec = ConsumerOffsetSpecification(OffsetType.LAST, None)
    elif args.offset == "next":
        offset_spec = ConsumerOffsetSpecification(OffsetType.NEXT, None)
    else:
        raise ValueError("Offset str must be either: first, last, next")
else:
    raise ValueError("Offset type must be either int or str")


async def receive():
    consumer = Consumer(host="localhost", port=5552, vhost="/", username="user", password="password")
    await consumer.create_stream(STREAM, exists_ok=True, arguments={
        "MaxLengthBytes": STREAM_RETENTION,
        "MaxAge": "5s"
    })

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(
        signal.SIGINT,
        lambda: asyncio.create_task(consumer.close())
    )

    async def on_message_callback(msg: AMQPMessage, context: MessageContext):
        stream = context.consumer.get_stream(context.subscriber_name)
        print(f"Got from stream {stream} subscriber {context.subscriber_name} message \"{msg}\" offset {context.offset}")

    print("Press control +C to close")
    await consumer.start()
    await consumer.subscribe(stream=STREAM, 
                             callback=on_message_callback, 
                             decoder=lambda b: b.decode(),
                             offset_specification=offset_spec,
                             properties={
                                 "single-active-consumer": "true" if args.single == True else "false",
                                 "name": args.name,
                                #  "super_stream": "my-test-stream-single"
                             })
    await consumer.run()

    await asyncio.sleep(1)

asyncio.run(receive())
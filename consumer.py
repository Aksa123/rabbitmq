from base import pika, conn, channel
from pprint import pprint
from argparse import ArgumentParser, ArgumentError
import os, sys

def main():

    parser = ArgumentParser(description="queue name")
    action_queue = parser.add_argument("--queue", type=str, default='')
    action_queue = parser.add_argument("--temp", type=bool, default=False)
    exchange_queue = parser.add_argument("--exchange", type=str, default='')

    args = parser.parse_args()
    print(args)

    queue = args.queue

    if args.temp == False and args.queue == '':
        raise ArgumentError(argument=action_queue, message="If temp = False then queue must be set")
    
    if args.temp == True:
        result = channel.queue_declare(queue='', exclusive=True)
        queue = result.method.queue
        channel.queue_bind(queue=queue, exchange=args.exchange, routing_key="test-key")

    def callback(ch, method, properties, body):
        print(f"Message received! {body.decode()}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

from base import pika, conn, channel
from argparse import ArgumentParser

parser = ArgumentParser(description="exchange name and message body")
parser.add_argument("--exchange", type=str)
parser.add_argument("--message", type=str)
parser.add_argument("--key", type=str, default="")
args = parser.parse_args()

channel.basic_publish(exchange=args.exchange,
                      routing_key=args.key,
                      body=args.message)

conn.close()

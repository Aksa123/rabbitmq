import pika
import pika.credentials


creds = pika.credentials.PlainCredentials(username="user", password="password")
conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, virtual_host="/", credentials=creds))
channel = conn.channel()

channel.queue_declare("queue_1")
channel.queue_declare("queue_2")
channel.queue_declare("queue_3")
channel.queue_declare("queue_4", durable=True)
channel.exchange_declare("fanout", exchange_type="fanout")
channel.exchange_declare("direct", exchange_type="direct")

channel.queue_bind(queue="queue_1", exchange="fanout")
channel.queue_bind(queue="queue_2", exchange="fanout")
channel.queue_bind(queue="queue_3", exchange="direct", routing_key="test-key")
channel.queue_bind(queue="queue_4", exchange="direct", routing_key="test-key")
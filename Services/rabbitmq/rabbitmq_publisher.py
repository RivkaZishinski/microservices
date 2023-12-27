import pika

from services.logger import Logger
from services.rabbitmq.rabbitmq_settings import RabbitMQSettings


class RabbitMQPublisher():
    def __init__(self, settings:RabbitMQSettings, logger):
        self.settings:RabbitMQSettings = settings
        self.conn = None
        self.channel = None
        self.logger = logger

    def connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.settings.host, port=self.settings.port))
        self.channel = self.conn.channel()

        #self.channel.exchange_declare(exchange=self.settings.exchagne, exchange_type=self.settings.exchange_type)
        self.channel.queue_declare(queue=self.settings.queue, durable=True)
        #self.channel.queue_bind(exchange=self.settings.exchagne, queue=self.settings.queue, routing_key=self.settings.routing_key)
    
    def clean_up(self):
        if self.channel is None:
            self.channel.close()

        if self.conn is None:
            self.conn.close()

    def publish(self, msg, headers={}):
        try:
            self.connect()
            
            self.channel.basic_publish(
                exchange=self.settings.exchagne,
                routing_key=self.settings.queue,
                body=msg,
                properties=pika.BasicProperties(
                    content_type='application/json',
                    content_encoding='utf-8',
                    headers=headers)
            )
        except Exception as e:
            self.logger.error(e)
            raise e
        finally:
            self.clean_up()
        
        

        

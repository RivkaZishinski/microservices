import time

import pika

from services.logger import Logger
from services.rabbitmq.rabbitmq_settings import RabbitMQSettings


class RabbitMQConsumer:
    def __init__(self, settings:RabbitMQSettings, retry_count:int, retry_delay:int, logger):
        self.settings:RabbitMQSettings = settings
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.conn = None
        self.channel = None
        self.logger = logger

    def connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.settings.host, port=self.settings.port))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=self.settings.queue, durable=True)
    
    def clean_up(self):
        try:
            if self.channel is None:
                self.channel.close()

            if self.conn is None:
                self.conn.close()
        except Exception as e:
            self.logger.error(e)

    def establish_connection(self):  
        retry_count:int = 0
        is_successful:bool = False

        while retry_count != self.retry_count and not is_successful:
            try:
                self.connect()     
                is_successful = True
            except Exception as e:
                self.logger.error(e)
                self.clean_up()
                retry_count += 1

                if retry_count == self.retry_count:
                    raise e
                    
                time.sleep(self.retry_delay * (retry_count + 1))

    def consume(self, callback):
        continue_consume = True 

        while(continue_consume):
            try:
                self.establish_connection()
                self.channel.basic_consume(queue=self.settings.queue, on_message_callback=callback, auto_ack=True)
                self.channel.start_consuming()
            except KeyboardInterrupt as e:
                self.logger.error(e)
                continue_consume = False
            except Exception as e:
                self.logger.error(e)
                self.establish_connection()
            finally:
                self.clean_up()




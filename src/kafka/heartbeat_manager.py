from kafka_manager import KafkaManager
from utils.helpers import Helpers
import datetime
import time
import threading
import logging


class HeartbeatManager():
    def __init__(self, kafka_heartbeat_producer:KafkaManager, heartbeat_interval, client_id):
        self.heartbeat_interval = heartbeat_interval
        self.client_id = client_id
        self.kafka_heartbeat_producer = kafka_heartbeat_producer
        self.helper = Helpers()

    def start_heartbeat_async(self):
        thr = threading.Thread(target=self.heartbeat_handler, args=(), kwargs={})
        thr.start()

    def heartbeat_handler(self):
        self.helper.set_interval(self.send_heartbeat_message,self.heartbeat_interval)

    def send_heartbeat_message(self):
        date = datetime.datetime.utcnow()
        date_ms = int(time.mktime(date.timetuple())) * 1000

        message_json = {"id":self.client_id, "alive": date_ms}
        message = {"messages": message_json}
        self.kafka_heartbeat_producer.send_messages(message)

    def stop(self):
        self.helper.stop_set_interval_thread()



import config
import pyinotify
import os
import pika

class LogMonitor(pyinotify.ProcessEvent):

    def __init__(self, filename, channel):
        self.fh = open(filename, 'r')
        self.channel = channel
        file_size = os.stat(filename).st_size
        self.fh.seek(file_size)

    def process_IN_MODIFY(self, event):
        line = self.fh.readline()
        self.channel.basic_publish(exchange='logs', routing_key='', body=line)

    # TODO - should handle logrotate, deletion, creation of a new file

if __name__ == "__main__":
    rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host']))
    channel = rabbit_connection.channel()
    channel.exchange_declare(exchange='logs', type='fanout')

    wm = pyinotify.WatchManager()

    mask = pyinotify.IN_MODIFY

    handler = LogMonitor(config.log_file, channel)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(config.log_file, mask, rec=True)
    notifier.loop()

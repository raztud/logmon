#!/usr/bin/env python
import pika
import smtplib
import config


def send_email(configuration, subject, message):
    from_addr = configuration['from']
    to_addr_list = configuration['to']
    cc_addr_list = configuration.get('cc', list())

    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(configuration['smtp_server'])
    server.starttls()
    server.login(configuration['username'], configuration['password'])
    errors = server.sendmail(from_addr, to_addr_list, message)
    server.quit()


def callback(ch, method, properties, body):
    print " [x] %r" % (body,)
    send_email(config.report['email'], 'Error', body)

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print ' [*] Waiting for logs. To exit press CTRL+C'

    channel.basic_consume(callback, queue=queue_name, no_ack=True)

    channel.start_consuming()

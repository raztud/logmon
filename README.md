logmon
======

Monitors an error log file

# Files

* monitor.py monitors the error log file specified in config.py (every  new line in the error file will be send out to a rabbit mq server)
* receiver.py subscribe to rabbitmq, get the messages and send out an email using the config.py
* config.py is the configuration file

# Installation

[Install rabbitmq](http://www.rabbitmq.com/install-debian.html)

sudo pip install -r requirements.txt



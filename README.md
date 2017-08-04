# README #

Picartopush is a simple cron-able script for sending push notifications via simplepush to your phone.

### How do I get set up? ###

Picartopush was written using Python 3.4 and requires the following modules:
* simplepush
* requests
* json
* urllib

You can set this up in a virtualenv if need be.

The first time you run `python picartopush.py` it will walk you through configuring it and create required files.
From there, you can then add running the script to your crontab. I recommend writing a simple shell script to do so, including invoking the virtualenv if required.

Have fun! Report any bugs!
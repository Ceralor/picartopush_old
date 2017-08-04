# README #

Picartopush is a simple cron-able script for sending push notifications via simplepush to your phone.

### How do I get set up? ###

Picartopush was written using Python 3.4 and requires the following modules:
* simplepush
* requests
* json

You can set this up in a virtualenv if need be.

You also will need to create the following two files in the directory picartopush.py runs in:

* online\_following.json
* config.json

Config.json is expected to be a standard JSON dictionary-type object containing the following:

* picarto\_bearer: This is the picarto API token you have, requiring the readpriv rights
* simplepush\_key: This is the unique key associated with your Simplepush app
* adult: boolean if you want adult streams
* gaming: boolean if you want gaming streams


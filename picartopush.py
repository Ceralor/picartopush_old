import requests, json, simplepush
config = {}
previous_online_following = []
try: 
    with open("config.json") as f:
        config = json.load(f)
except:
    print("File 'config.json' must be present!")
    exit()
try:
    with open("online_following.json","r") as f:
        previous_online_following = json.load(f)
except:
    with open("online_following.json","w") as f:
        json.dump({},f)
    print("File 'online_following.json' has been created for you.")
headers = {'accept':'application/json','authorization':'Bearer %s' % (config['picarto_bearer'])}
r = requests.get('https://api.picarto.tv/v1/user',headers=headers)
following = r.json()['following']
following_ids = [ x['user_id'] for x in following ]
url = 'https://api.picarto.tv/v1/online?adult=%s&gaming=%s' % (config['adult'],config['gaming'])
r = requests.get(url,headers=headers)
online_channels = r.json()
online_following = [ x for x in online_channels if x['user_id'] in following_ids ]
online_following
with open("online_following.json","w") as f:
    json.dump([ x['name'] for x in online_following ],f)
for channel in [x for x in online_following if x['name'] not in previous_online_following]:
    nsfw_string = ' (NSFW)' if channel['adult'] else ''
    title = 'Picarto user %s online!%s' % (channel['name'],nsfw_string)
    msg = '%s is now streaming%s, check it out! https://picarto.tv/%s' % (channel['name'],nsfw_string,channel['name'])
    simplepush.send(config['simplepush_key'],title,msg)
    print("%s is online!" % (channel['name']))

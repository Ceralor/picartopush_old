import requests, json, simplepush

def get_online_following(config):
    headers = {'accept':'application/json','authorization':'Bearer %s' % (config['picarto_bearer'])}
    r = requests.get('https://api.picarto.tv/v1/user',headers=headers)
    following = r.json()['following']
    following_ids = [ x['user_id'] for x in following ]
    url = 'https://api.picarto.tv/v1/online?adult=%s&gaming=%s' % (config['adult'],config['gaming'])
    r = requests.get(url,headers=headers)
    online_channels = r.json()
    online_following = [ x for x in online_channels if x['user_id'] in following_ids ]
    with open("online_following.json","w") as f:
        json.dump([ x['name'] for x in online_following ],f)
    return online_following
def send_online_following_simplepush(config,online_following,previous_online_following):
    for channel in [x for x in online_following if x['name'] not in previous_online_following]:
        nsfw_string = ' (NSFW)' if channel['adult'] else ''
        title = 'Picarto user %s online!%s' % (channel['name'],nsfw_string)
        msg = '%s is now streaming%s, check it out! https://picarto.tv/%s' % (channel['name'],nsfw_string,channel['name'])
        simplepush.send(config['simplepush_key'],title,msg)
        print("Sent notification about %s" % (channel['name']))

def make_online_following_file():
    with open("online_following.json","w") as f:
        json.dump({},f)

def setup():
    from urllib.parse import quote_plus as qp
    make_online_following_file()
    config = {}
    redirect_uri = "https://puffydrake.com/oauth.php"
    print('First, visit https://oauth.picarto.tv/clients and create a new client named whatever. set the return URI to %s' % (redirect_uri))
    print('Then enter the client ID and client secret')
    client_id = input("client_id: ")
    client_secret = input("client_secret: ")
    print("Visit the below URL, then paste the 'code' as prompted")
    print('https://oauth.picarto.tv/authorize?response_type=code&client_id=%s&redirect_uri=%s&scope=readpriv' % (client_id, qp(redirect_uri)))
    code = input("> ")
    data = { "grant_type" : "authorization_code", "code" : code, "redirect_uri": redirect_uri, "client_id" : client_id, "client_secret" : client_secret}
    r = requests.post('https://oauth.picarto.tv/token', data=data)
    if r.status_code != 200:
        print("Something went wrong. Check out below and try again.")
        print(r.text)
        exit()
    access_token = r.json()['access_token']
    config['picarto_bearer'] = access_token
    print("Great! Now enter your Simplepush API key.")
    simplepush_key = input("> ")
    config['simplepush_key'] = simplepush_key
    config["adult"] = True
    config["gaming"] = False
    print("Great! We've defaulted to show adult streams but not gaming. You can change this in config.json later.")
    with open("config.json","w") as f:
        json.dump(config,f)
def main():
    config = {}
    previous_online_following = []
    try: 
        with open("config.json") as f:
            config = json.load(f)
    except:
        print("File 'config.json' must be present!")
        print("I'll help you set up now!")
        setup()
        exit()
    try:
        with open("online_following.json") as f:
            previous_online_following = json.load(f)
    except:
        make_online_following_file()
        print("File 'online_following.json' has been created for you.")
    online_following = get_online_following(config)
    for channel in online_following:
        print("%s is online!" % (channel['name']))
    send_online_following_simplepush(config,online_following,previous_online_following)
if __name__ == "__main__":
    main()


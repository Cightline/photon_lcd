
import requests
import os
import os.path
import json
import argparse

home          = os.getenv('HOME')
write_dir     = '%s/.cache/photon_lcd' % (home)
config_path   = '%s/.config/photon_lcd/config.json' % (home)

with open(config_path, 'r') as cfg:
    config = json.load(cfg)



if not os.path.exists(write_dir):
    os.makedirs(write_dir)
    print('created %s' % (write_dir))


api_key         = config['api_key']
state           = config['state']
city            = config['city']
weather_dir     = '%s/.cache/photon_lcd' % (home)
device          = config["id"]
access_token    = config['access_token']


def update(title, message, is_alert):
    
    json_data = json.dumps({'title':title, 'message':message, 'is_alert':int(is_alert)})

    response = requests.post('https://api.particle.io/v1/devices/%s/update' % (device), {'access_token':access_token, 'args':json_data})

    if response.status_code != 200:
        print('wrong return code: %s' % (response.status_code))
        print(response.text)


    print(response)
    print(response.content)
    print(json_data)

    if response.json()['return_value'] == 1:
        print('successfully sent message')



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()


def write_to_file(directory, name, data):
    with open('%s/%s' % (directory, name), 'w') as f:
        f.write(data)






if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--message', action='store',      help='message to send to LCD')
    parser.add_argument('--title',   action='store',      help='title of the message')
    parser.add_argument('--alert',   action='store_true', help='marks the message as an alert', default=False)

    args = parser.parse_args()


    if args.message and not args.title:
        print('You forgot --title')
        exit()

    if args.message and args.title:
        update(args.title, args.message, args.alert)

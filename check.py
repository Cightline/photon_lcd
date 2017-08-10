
import requests
import os
import os.path
import json
import re

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

alert_url       = 'http://api.wunderground.com/api/%s/alerts/q/%s/%s.json' % (api_key, state, city)
condition_url   = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (api_key, state, city)
forecast_url     = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json' % (api_key, state, city)


def update(temp_f, weather):

    json_data = json.dumps({'temp_f':temp_f, 'weather':weather.lower()})

    response = requests.post('https://api.particle.io/v1/devices/%s/update' % (device), {'access_token':access_token, 'args':json_data})

    if response.status_code != 200:
        print('wrong return code: %s' % (response.status_code))
        print(response.text)


    #print(response)
    #print(response.content)
    #print(json_data)

    if response.json()['return_value'] == 1:
        print('successfully sent weather information')


def update_alert(alert_is_current, alert_message):

    json_data = json.dumps({'alert_is_current':alert_is_current, 'alert_message':alert_message})

    response = requests.post('https://api.particle.io/v1/devices/%s/update_alert' % (device), {'access_token':access_token, 'args':json_data})

    if response.status_code != 200:
        print('wrong return code: %s' % (response.status_code))
        print(response.text)


    #print(response)
    #print(response.content)
    #print(json_data)

    if response.json()['return_value'] == 1:
        print('successfully sent alert information')



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()


def write_to_file(directory, name, data):
    with open('%s/%s' % (directory, name), 'w') as f:
        f.write(data)



c = get_page(condition_url)['current_observation']



alert_data = []
alert_string = 'no_alert'

data = (get_page(alert_url)['alerts'])
    
for alert in data:
    alert_data.append(alert['type'])


if alert_data:
    alert_string = '/'.join(alert_data)
    update_alert(alert_is_current=True, alert_message=str(alert_string))


else:
    update_alert(alert_is_current=False, alert_message=str(alert_string))

f = get_page(forecast_url)

print(f)

update(str(int(c['temp_f'])), str(c['weather']))




write_to_file(write_dir, 'weather.json', json.dumps(c))
write_to_file(write_dir, 'alerts.json', json.dumps(data))
write_to_file(write_dir, 'forecast.json', json.dumps(f))
#update(str(c['temp_f']), str(c['weather']), "ALERT")


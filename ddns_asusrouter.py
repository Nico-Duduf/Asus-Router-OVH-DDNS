from base64 import b64encode
import requests
import yaml
import os
from RouterInfo import RouterInfo

def dnsUpdate(host, ip, user, password):
    url = 'https://www.ovh.com/nic/update'
    login = b64encode(
        bytes(user+':'+password, 'utf-8')
    ).decode('utf-8')
    params = {
        'system': 'dyndns',
        'hostname': host,
        'myip': ip,
    }
    headers = {
        'Authorization': 'Basic ' + login,
        'User-Agent': 'RxKaboratory - RXDDNSSynologyClient - 0.0.1',
    }

    response = requests.get(url, params=params, headers=headers)
    print(response.text)

if __name__ == "__main__":
    # Get config
    configData = ()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+'/config.yml', 'r', encoding='utf8') as configFile:
        configData = yaml.safe_load(configFile)
    
    # Get current public IP
    router = configData['router']
    ri = RouterInfo(router['address'], router['username'], router['password'])
    wanInfo = ri.get_status_wan()
    publicIP = wanInfo['ipaddr'].replace("'", '')
    print('Current public Ip: '+publicIP)

    # Send the update
    hosts = configData['hosts']
    for host in hosts:
        if (hosts[host]['current']) == publicIP:
            print(host+': IP already set.')
            continue
        dnsUpdate(host, publicIP, hosts[host]['username'], hosts[host]['password'])
        hosts[host]['current'] = publicIP

    # Cache current IP
    configData['hosts'] = hosts
    with(open(dir_path+'/config.yml', 'w', encoding='utf8')) as config:
        yaml.dump(configData, config)
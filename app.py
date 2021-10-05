import requests
from flask import Flask, request, json
import os

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST'])
def parse_request():
    print(request.args)
    if 'cmd' in request.args:
        if request.args['cmd'] == '1':
            gude_api(request.args['device'], request.args['value'])
        elif request.args['cmd'] == '2':
            status_api(request.args['device'])
    return "Hello"


def status_api(device):
    if device == 'volt':
        payload = {'components':'1'}
        response = requests.get('http://10.140.1.60/statusjsn.js', params=payload)
        json_resp = response.json()


def gude_api(device, value):
    ip = 'http://10.140.1.60/ov.html'
    mount_ip = '10.140.1.37'
    if device == 'volt':
        payload = {'cmd': '1', 'p': '3', 's': value}
        response = requests.get(ip, params=payload)
        print(response.text)

    elif device == 'mount':
        ping = os.system('ping -c 1' + mount_ip)
        if ping != 0:
            switch_payload = {'cmd': '5', 'p': '2', 'a1': '1', 'a2': '0', 's': '2'}
            switch_response = requests.get(ip, params=switch_payload)


if __name__ == '__main__':
    app.run()

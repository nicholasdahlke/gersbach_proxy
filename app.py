import string
import flask
import requests
from flask import Flask, request, json
import os
from dataclasses import dataclass

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST'])
def parse_request():
    print(request.args)
    if 'cmd' in request.args:
        if request.args['cmd'] == '1':
            gude_api(request.args['device'], request.args['value'])
        elif request.args['cmd'] == '2':
            return status_api(request.args['device'])
    return "Error"


@dataclass
class StatusResp:
    name: string
    value: bool


ip = 'http://10.140.1.60/ov.html'
mount_ip = '10.140.1.37'


def status_api(device):
    if device == 'volt':
        return status_api_call(3)

    elif device == 'mount':
        resp = StatusResp(name='Montierung', value=False if os.system('ping -c 1 ' + mount_ip) else True)
        return flask.jsonify({'device_name':resp.name,'device_state': resp.value})

    elif device == 'pc':
        return status_api_call(1)

    elif device == 'free':
        return status_api_call(4)

    return "error"


def status_api_call(value):
    payload = {'components': '1'}
    response = requests.get('http://10.140.1.60/statusjsn.js', params=payload)
    json_resp = response.json()
    resp = StatusResp(name=json_resp['outputs'][value - 1]['name'], value=json_resp['outputs'][value - 1]['state'])
    resp_dict = {'device_name': resp.name, 'device_state': bool(resp.value)}
    return flask.jsonify(resp_dict)


def switch_api(device_num, value):
    payload = {'cmd': '1', 'p': device_num, 's': value}
    response = requests.get(ip, params=payload)
    return "Success"


def gude_api(device, value):
    if device == 'volt':
        switch_api('3', value)

    elif device == 'pc':
        switch_api('3', value)

    elif device == 'free':
        switch_api('4', value)

    elif device == 'mount':
        ping = os.system('ping -c 1 ' + mount_ip)
        if ping != 0:
            switch_payload = {'cmd': '5', 'p': '2', 'a1': '1', 'a2': '0', 's': '2'}
            switch_response = requests.get(ip, params=switch_payload)


if __name__ == '__main__':
    app.run()

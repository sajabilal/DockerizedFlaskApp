from flask import Flask, request, json, jsonify
from flask_limiter import Limiter,util
import ipaddress

app = Flask(__name__)
limiter = Limiter(key_func=util.get_remote_address, app= app)
accepted = 0
blocked = 0
CIDRs = 0
blocked_CIDRs = [{}]


def check_validity(data):
    if 'CIDR' in data and 'ttl' in data:
        return True
    else:
        return False


def check_ip(ip):
    global accepted
    global blocked
    if not blocked_CIDRs:
        for i in blocked_CIDRs:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(blocked_CIDRs.CIDR):
                blocked = blocked +1
                return True
            else:
                accepted = accepted +1
                return False
    else:
        accepted = accepted + 1
        return False


@app.route('/')
@limiter.limit("3 per minute")
def main_page():
    ip = jsonify({'ip': request.remote_addr}), 200
    if check_ip(ip) is False:
        return 'welcome to main webpage  :) :)  '
    else:
        return 'you are blocked'


@app.route('/healthcheck')
def healthcheck():
    ip = jsonify({'ip': request.remote_addr}), 200
    if check_ip(ip) is False:
        return 'page is up  '
    else:
        return 'you are blocked'


@app.route('/stats')
def stats():
    ip = jsonify({'ip': request.remote_addr}), 200
    if check_ip(ip) is False:
        global accepted
        global blocked
        stat = { 'accepted': accepted, 'blocked': blocked, 'CIDRs': len(blocked_CIDRs)-1}
        return json.dumps(stat)
    else:
        return 'you are blocked'


@app.route('/block', methods=['POST'])
def block():
    ip = jsonify({'ip': request.remote_addr}), 200
    print(ip)
    print(blocked_CIDRs)
    if check_ip(ip) is False:
        added_data = request.get_json()
        valid = check_validity(added_data)
        if valid:
            blocked_CIDRs.insert(0, {'CIDR': added_data['CIDR'], 'ttl': added_data['ttl']})
            print(blocked_CIDRs)
            return "Done"
        else:
            return "error"
    else:
        return 'you are blocked'


app.run(host='0.0.0.0', port=8080)

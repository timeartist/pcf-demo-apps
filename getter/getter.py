from os import getenv
from json import loads, dumps

from flask import Flask, render_template
from redis import Redis

app = Flask(__name__)

@app.route('/')
def show():
    return render_template('display.html')

@app.route('/data')
def data():
    return dumps(redis.lrange('form-inputs', 0, -1))


def make_redis():
    try:
        service_env_vars = loads(getenv('VCAP_SERVICES'))['redislabs'][0]
        credentials = service_env_vars['credentials']
        host = credentials['ip_list'][0]
        port = credentials['port']
        password = credentials['password']

        return Redis(host=host, port=port, password=password)
    except:
        return Redis()

redis = make_redis()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

from os import getenv
from uuid import uuid4
from json import loads
from time import sleep
import logging

from redis import Redis, ConnectionError
from flask import Flask

DATA_SIZE = 1000
SLEEP_INTERVAL = 1
MAX_RETRY_TIMES = 30

app = Flask(__name__)
mode = ''


@app.route('/')
def test(attempt=0):
    guid = uuid4()

    try:
        redis.set(guid, 'x'*DATA_SIZE)
    except:
        if attempt == MAX_RETRY_TIMES:
            raise

        attempt += 1
        sleep(SLEEP_INTERVAL)
        test(attempt)

    return str(guid)

@app.route('/mode')
def mode():
    return mode

def make_redis():
    try:
        global mode
        env = getenv('VCAP_SERVICES')

        if env is None:
            raise ConnectionError

        service_env_vars = loads(env)['redislabs-enterprise-cluster'][0]
        credentials = service_env_vars['credentials']
        dns = credentials['host']
        ip = credentials['ip_list'][0]
        port = credentials['port']
        password = credentials['password']

        redis = Redis(dns, ip, port, password)
        redis.ping()
        mode = 'dns'
        logging.info('using dns: ' + dns)
        return redis
    except:
        try:
            redis = Redis(host=ip, port=port, password=password)
            redis.ping()
            mode = 'ip'
            logging.info('using ip: ' + ip)
            return redis
        except:
            logging.info('using localhost')
            redis = Redis()
            mode = 'localhost'
            return redis

redis = make_redis()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

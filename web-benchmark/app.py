from os import getenv
from uuid import uuid4

from redis import Redis, ConnectionError
from flask import Flask

DATA_SIZE = 1000

app = Flask(__name__)


@app.route('/')
def test():
    guid = uuid4()
    redis.set(guid, 'x'*DATA_SIZE)

    return str(guid)

def make_redis():
    try:
        env = getenv('VCAP_SERVICES')

        if env is None:
            raise ConnectionError

        service_env_vars = loads(env)['redislabs-enterprise-cluster'][0]
        credentials = service_env_vars['credentials']
        dns = credentials['']
        ip = credentials['ip_list'][0]
        port = credentials['port']
        password = credentials['password']

        redis = Redis(dns, ip, port, password)
        redis.ping()
        return redis
    except ConnectionError:
        try:
            redis = Redis(host=ip, port=port, password=password)
            redis.ping()
            return redis
        except:
            redis = Redis()
            redis.ping()
            return redis

redis = make_redis()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

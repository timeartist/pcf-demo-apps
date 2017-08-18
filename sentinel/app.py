from os import getenv
from uuid import uuid4
from json import loads, dumps
from time import sleep
import logging

from redis import Redis, ConnectionError
from redis.sentinel import Sentinel
from flask import Flask


app = Flask(__name__)
mode = ''
sentinel = None
db_name = ''


@app.route('/')
def test():
    env = getenv('VCAP_SERVICES')
    credentials = loads(env)['redislabs'][0]['credentials']
    dns = credentials['host']
    ip = credentials['ip_list'][0]
    port = credentials['port']
    password = credentials['password']
    name = credentials['name']

    sentinel = Sentinel([(ip, 8001)])

    logging.info(sentinel)
    logging.info(sentinel.discover_master(name))



    return dumps(sentinel.discover_master(name))


# @app.route('/master')
# def mode():
#     return dumps(sentinel.discover_master(db_name))
#
# def make_redis():
#     #try:
#     global mode
#     global sentinel
#     global db_name
#
#     env = getenv('VCAP_SERVICES')
#
#     if env is None:
#         raise ConnectionError
#
#     service_env_vars = loads(env)['redislabs'][0]
#     credentials = service_env_vars['credentials']
#     dns = credentials['host']
#     ip = credentials['ip_list'][0]
#     port = credentials['port']
#     password = credentials['password']
#     name = credentials['name']
#
#     logging.info('name: ' + name)
#
#     sentinel = Sentinel([('rpsentinel.app.demo.pcf.redis.ninja', 80)])
#     logging.info(sentinel.discover_master(name))
#
#     # redis = Redis(dns, ip, port, password)
#     # redis.ping()
#     # mode = 'dns'
#     # logging.info('using dns: ' + dns)
#     # return redis
#     # except:
#     #     try:
#     #         redis = Redis(host=ip, port=port, password=password)
#     #         redis.ping()
#     #         mode = 'ip'
#     #         logging.info('using ip: ' + ip)
#     #         return redis
#     #     except:
#     #         logging.info('using localhost')
#     #         redis = Redis()
#     #         mode = 'localhost'
#     #         return redis
#
# redis = make_redis()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

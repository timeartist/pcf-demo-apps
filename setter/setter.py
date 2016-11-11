from os import getenv
from json import loads

from flask import Flask, request, render_template
from redis import Redis

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def submit():
    print request.form
    resp = redis.rpush('form-inputs', request.form['input-text'])
    return render_template('form.html', success=True)

@app.route('/clear')
def clear():
    redis.flushdb()
    return 'DB Cleared'

def make_redis():
    try:
        service_env_vars = loads(getenv('VCAP_SERVICES'))['redislabs-enterprise-cluster'][0]
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

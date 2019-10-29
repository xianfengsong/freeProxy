from flask import Flask
from flask_pymongo import PyMongo
import random

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://proxy:proxy@127.0.0.1:9000,127.0.0.1:9001,127.0.0.1:9002/free_proxy"
mongo = PyMongo(app)
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/proxy/<requestid>/<protocol>',methods=['GET'])
def proxy(requestid,protocol):
    #查询stable_proxy
    proxies = list(mongo.db.stable_proxy.find({'protocol':protocol}))
    if proxies is None or len(proxies) == 0:
        #查询fresh_proxy
        proxies = list(mongo.db.stable_proxy.find({'protocol':protocol}))
    if proxies is not None and len(proxies) != 0:
        proxy = random.choice(list(proxies))
        return proxy['address']
    else:   
        return "None"

if __name__ == "__main__":
    app.run(debug=True,host='10.221.128.67')
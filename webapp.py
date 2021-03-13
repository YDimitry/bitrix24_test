from flask import Flask
from flask import request
import json
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    data ={}
    if request.method == 'POST':
        data = request.form
    return(json.dumps(data))

if __name__ == '__main__':
    app.run()
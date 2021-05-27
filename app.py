from flask import Flask, jsonify, make_response, render_template
import time
from collections import namedtuple
from flask_cors import *

app = Flask(__name__)

CORS(app, supports_credentials=True)


def timestamp(timestring: str):
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S')) * 1000  # 1482286976.0


def read_file(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    return data


def handle(path: str, target: str, time: str):
    md = read_file(path)
    targets = [target.strip() for target in md[0].strip('|').split('|')]
    Log = namedtuple('Log', targets)
    target_list = []
    for line in md[2:]:
        values = [target.strip() for target in line.strip('|').split('|')]
        line = Log(*values)
        target_list.append([int(timestamp(getattr(line, time))), int(getattr(line, target))])
    return target_list


@app.route('/json/<target>', methods=['GET'])
def json(target):
    data = handle('VmRss.md', target, 'realtime')
    # print(data)
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8089)

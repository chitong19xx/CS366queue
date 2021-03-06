from flask import Flask
from flask import request
import json

DATA_PATH = "data.txt"

def get_data():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except IOError:
        pass
    return {'size': 0, 'list': []}

def set_data(d):
    with open(DATA_PATH, "w") as f:
        json.dump(d, f)

def get_number_in_queue():
    return get_data()['size']

def set_number_in_queue(num):
    old_data = get_data()
    old_data['size'] = num
    set_data(old_data)

def get_queue_list():
    return get_data()['list']

app = Flask(__name__)
@app.route('/')
def report_queue_size():
    lst = ""
    for unhappyPerson in get_queue_list():
        lst += '<li>' + unhappyPerson + '</li>'
    return ("<p>The queue has "+str(get_number_in_queue())+" people in it.</p>"
        "<p>This is who they are:</p>"
        "<ol>"+lst+"</ol>")

@app.route('/change/<int:size>')
def change_queue_size(size):
    set_number_in_queue(size)
    return "Done"

@app.route('/set_list', methods=['POST'])
def set_list():
    json_data = request.get_json(force=True)
    data = get_data()
    data['list'] = json_data['list']
    set_data(data)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

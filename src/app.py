from flask import Flask

app = Flask(__name__)

counter = 0

@app.route('/')
def index():
    global counter
    counter += 1
    return 'Hello from root route! You are ' + str(counter) + ' visitor!'

@app.route('/about')
def about():
    return 'Hello from ''About'' route'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')
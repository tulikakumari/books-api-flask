from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello world'

app.run(port=5000)
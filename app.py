from flask import Flask, request
from algorithm import to_row
import json

app = Flask(__name__)

@app.route("/")
def home():
    return json.dumps({'response': 'use /tree with GET parameter «text»'})

@app.route("/tree")
def tree():
    text = request.args.get('text')
    return to_row(text)
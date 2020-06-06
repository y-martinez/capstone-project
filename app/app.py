#!/usr/bin/env python3

import boto3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/result')
def result():
    return render_template('templates/index.html')

@app.route('/',methods=["POST"])
def index():
    return render_template('templates/index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
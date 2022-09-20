from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jungletube

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/api/login')
def login():
    return

@app.route('/api/logout')
def logout():
    return

@app.route('/api/signin')
def signin():
    return

@app.route('/api/upload')
def upload():
    return

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
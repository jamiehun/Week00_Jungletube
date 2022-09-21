from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import math

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jungletube
row_count = db.users.estimated_document_count()



# DB에 저장된 video 보여주는 역할
@app.route('/')
def showVideo():
    # db.users에서 category 찾아서 week만 분류해놓기
    category_list = []
    for name in db.users.find():
        temp = name['category']
        if temp not in category_list:
            category_list.append(temp)
        category_list.sort(reverse=True)
    
    # 분류된 week를 기준으로 like 순으로 정렬하여 리스트 만들기
    # 기존 : {'week2': 
    #          [{'category': 'week2', 'comment': 'dijkstra', 'url': 'https://youtu.be/611B-9zk2o4', 'like': 3}], 
    #        'week0': 
    #          [{'category': 'week0', 'comment': 'session_cookie','url': 'https://youtu.be/tosLBcAX1vk', 'like': 2}, 
    #           {'category': 'week0', 'comment': 'jinja_Flask', 'url': 'https://youtu.be/NKJV0ekmo4U', 'like': 1}, 
    #           {'category': 'week0', 'comment': 'cookie_token', 'url': 'https://youtu.be/GhrvZ5nUWNg', 'like': 0}]}
    dict = {}
    card_count = {}
    for i in category_list:
        # 비디오 리스트 세기
        video_list = list(db.users.find({'category' : i}, {'_id': 0}).sort('like', -1))
        dict[i] = video_list #
        
        # 비디오 개수에 대한 정보 확인
        videoCount = len(video_list) # 비디오 개수 세기
        collectionCount = math.ceil(videoCount / 4) # 비디오 개수 4개로 자르기
        dummyCount = 4 - (videoCount % 4) # 비디오 개수 중 4의 배수가 아닌 수에 대한 dummy값 확인
        card_count[i] = {'collectionCount' : collectionCount, 'dummyCount' : dummyCount, 'cardCount' : videoCount}
        
    # dict 값, dummy_count 값, 
    return render_template('child_jinja2.html', dict = dict, card_count = card_count)

@app.route('/api/login')
def login():
    return

@app.route('/api/logout')
def logout():
    return

@app.route('/api/signin')
def signin():
    return

# 업로드 하기
@app.route('/api/upload')
def upload():
    return

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
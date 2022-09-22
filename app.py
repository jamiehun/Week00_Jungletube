from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token,
    get_jwt_identity, get_jwt,
    set_access_cookies, unset_jwt_cookies
)

from datetime import timedelta, timezone, datetime

import bcrypt
from pymongo import MongoClient
import math

app = Flask(__name__)

app.config["JWT_TOKEN_LOCATION"] = ['cookies']

app.config["JWT_SESSION_COOKIE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)

app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_COOKIE_SECURE"] = False

app.config['JWT_SECRET_KEY'] = 'junglekim'

jwt = JWTManager(app)

client = MongoClient('mongodb://cho:cho@13.124.49.24', 27017)
db = client.jungletube


@app.after_request
def refresh_expiring_jwts(resp):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))

        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(resp, access_token)

        return resp
    except (RuntimeError, KeyError):
        return resp

@app.route('/')
def main():
    # db.cards에서 category 찾아서 week만 분류해놓기
    category_list = []
    for name in db.cards.find():
        temp = name['category']
        if temp not in category_list:
            category_list.append(temp)
        category_list.sort(reverse=True)

    # 분류된 week를 기준으로 like 순으로 정렬하여 리스트 만들기
    dict = {}
    card_count = {}
    for i in category_list:
        # 비디오 리스트 세기
        video_list = list(db.cards.find(
            {'category': i}, {'_id': 0}).sort('like', -1))
        dict[i] = video_list

        # 비디오 개수에 대한 정보 확인
        videoCount = len(video_list)  # 비디오 개수 세기
        collectionCount = math.ceil(videoCount / 4)  # 비디오 개수 4개로 자르기
        # 비디오 개수 중 4의 배수가 아닌 수에 대한 dummy값 확인
        def dummyCount(x): return (4 - (x % 4)) if x != 4 else 0
        card_count[i] = {'collectionCount': collectionCount, 'dummyCount': dummyCount(
            videoCount), 'cardCount': videoCount}

    return render_template('child.html', dict=dict, card_count=card_count)


@app.route('/api/login', methods=['POST'])
def login():
    receive_id = request.form['give_id']
    receive_pwd = request.form['give_pwd']

    searched_id = db.users.find_one({'id': receive_id})

    if searched_id == None: 
        return jsonify({"msg": "가입하지 않은 ID"}), 400
    else:
        byte_pwd = receive_pwd.encode('UTF-8')
        origin_pwd = bytes.fromhex(searched_id['password'])

        if bcrypt.checkpw(byte_pwd, origin_pwd):
            access_token = create_access_token(identity=receive_id)

            resp = jsonify({'result': 'success'})
            set_access_cookies(resp, access_token)

            return resp

        else: 
            return jsonify({"msg": "잘못된 비밀번호"}), 400

    return jsonify({'result': 'success', 'token': access_token})

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'result': 'success'})
    unset_jwt_cookies(resp)

    return resp


@app.route('/api/signin', methods=['POST'])
def signin():
    receive_id = request.form['give_id']
    receive_pwd = request.form['give_pwd']
    receive_nick = request.form['give_nick']

    byte_pwd = receive_pwd.encode('UTF-8')
    cliper_pwd = bcrypt.hashpw(byte_pwd, bcrypt.gensalt()).hex()

    searched_id = db.users.find_one({'id': receive_id})

    if searched_id != None:
        pass
    else:
        db.users.insert_one(
            {'id': receive_id, 'password': cliper_pwd, 'nickname': receive_nick})

    return jsonify({'result': 'success'})


@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload():
    receive_category = request.form['give_category']
    receive_url = request.form['give_url']
    receive_comment = request.form['give_comment']

    db.cards.insert_one({'category': receive_category,
                        'url': receive_url, 'comment': receive_comment, 'like': 0})

    return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
@jwt_required()
def like():
    receive_url = request.form['give_url']

    searched_url = db.cards.find_one({'url': receive_url})

    new_like = searched_url['like'] + 1

    db.cards.update_one({'url': receive_url}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
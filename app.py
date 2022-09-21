from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import bcrypt
from pymongo import MongoClient

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "junglekim"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400 # 초 단위
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
jwt = JWTManager(app)

app.secret_key = "key"

client = MongoClient('mongodb://cho:cho@13.124.49.24', 27017) 
db = client.jungletube

@app.route('/')
def main():
    return render_template('maincho.html')

@app.route('/loginpage')
def logmain():
    return render_template('loginMain.html')

@app.route('/api/login', methods=['POST'])
def login():
    receive_id = request.form['give_id']
    receive_pwd = request.form['give_pwd']

    searched_id = db.users.find_one({'id':receive_id})
    
    if searched_id == None:     # 회원가입 되지 않은 ID 오류
        return jsonify({"msg": "가입하지 않은 ID"}), 400
    else:
        byte_pwd = receive_pwd.encode('UTF-8')
        origin_pwd = bytes.fromhex(searched_id['password'])

        if bcrypt.checkpw(byte_pwd, origin_pwd):
            access_token = create_access_token(identity=receive_id)     # 엑세스 토큰 발행
        else:       # 잘못된 비밀번호 오류
            return jsonify({"msg": "잘못된 비밀번호"}), 400

    return jsonify({'result':'success', 'token':access_token})

@app.route('/api/logout', methods=['GET'])
@jwt_required()
def logout():
        
    return jsonify({'result':'success'})

@app.route('/api/signin', methods=['POST'])
def signin():
    receive_id = request.form['give_id']
    receive_pwd = request.form['give_pwd']
    receive_nick = request.form['give_nick']
    error_n = 0

    byte_pwd = receive_pwd.encode('UTF-8')
    cliper_pwd = bcrypt.hashpw(byte_pwd, bcrypt.gensalt()).hex()

    searched_id = db.users.find_one({'id': receive_id})

    if searched_id != None:         # ID가 중복이면
        error_n = 1
    else:
        db.users.insert_one({'id': receive_id, 'password': cliper_pwd, 'nickname': receive_nick})

    return jsonify({'result':'success', 'error': error_n})

# @app.route('/api/upload', methods=['POST'])
# def upload():
#     return

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
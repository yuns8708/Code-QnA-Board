from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SECRET_KEY = 'CODEQNA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.kenusfb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.code_qna_board


# 메인 페이지
@app.route('/')
def home():
    QnA_list = list(db.miniproject.find({}))
    return render_template('index.html', QnA_list=QnA_list)


# 로그인
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 회원가입
@app.route('/register')
def register():
    msg = request.args.get("msg")
    return render_template('register.html', msg=msg)


# 로그인 서버
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 6)  # 로그인 6시간 유지(만료시간)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 입력 정보 저장
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    usernick_receive = request.form['usernick_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "usernick": usernick_receive,  # 닉네임
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 아이디 중복 체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 닉네임 중복 체크
@app.route('/sign_up/check_dup_nick', methods=['POST'])
def check_dup_nick():
    usernick_receive = request.form['usernick_give']
    exists = bool(db.users.find_one({"usernick": usernick_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 글쓰기 페이지
@app.route('/write')
def write():
    return render_template('write.html')


# 게시글 페이지
@app.route('/detail/<id>')
def detail_page(id):
    return render_template('detail.html', id=id)


# 게시글 페이지 데이터 요청
@app.route("/data/", methods=["GET"])
def detail_get():
    qna_list = list(db.miniproject.find({}, {'_id': False}))
    print(qna_list)
    return jsonify({'qna': qna_list})


# html/CSS 페이지
@app.route('/html_CSS')
def html_CSS():
    QnA_list = list(db.miniproject.find({}, {'_id': False}))
    return render_template('html_CSS.html', QnA_list=QnA_list)


# Javascript 페이지
@app.route('/Javascript')
def Javascript():
    QnA_list = list(db.miniproject.find({}, {'_id': False}))
    return render_template('Javascript.html', QnA_list=QnA_list)


# Python 페이지
@app.route('/Python')
def Python():
    QnA_list = list(db.miniproject.find({}, {'_id': False}))
    return render_template('Python.html', QnA_list=QnA_list)


# 글쓰기 페이지 인풋값
@app.route("/api/write", methods=["POST"])
def write_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    category_receive = request.form['category_give']
    fileUpload_receive = request.form['fileUpload_give']

    QnA_list = list(db.miniproject.find({}, {'_id': False}))
    count = len(QnA_list) + 1

    # done : 게시글 삭제유무 판단에 사용,    num : 게시글 고유 번호 확인용
    doc = {'done': 0, 'num': count, 'title': title_receive, 'content': content_receive, 'category': category_receive,
           'fileUpload': fileUpload_receive}
    db.miniproject.insert_one(doc)

    return jsonify({'msg': '작성 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.lo2ev.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.firstweekproject

# 메인 페이지
@app.route('/')
def home():
    QnA_list = list(db.miniproject.find({}))
    return render_template('index.html',QnA_list=QnA_list)


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
    return jsonify({'qna':qna_list})


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
    doc = {'done':0,'num':count, 'title': title_receive, 'content': content_receive, 'category':category_receive, 'fileUpload':fileUpload_receive}
    db.miniproject.insert_one(doc)

    return jsonify({'msg': '작성 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn


@app.route('/')     # 127.0.0.1:5000
def index():
    return render_template('index.html')
    # return "<h1>Welcome~ 방문을 환영합니다.</h1>"


@app.route('/member_list')
def member_list():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('member_list.html', rs=rs)


@app.route('/member_view/<string:id>/')
def member_view(id):    # mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % id
    cur.execute(sql)
    rs = cur.fetchone()     # 해당 1개의 자료를 반환
    conn.close()
    return render_template('member_view.html', rs=rs)


app.run(debug=True)

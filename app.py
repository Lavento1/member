from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "rlawlsxo"     # 암호키 설정


def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn


@app.route('/')     # 127.0.0.1:5000
def index():
    if 'userID' in session:     # session에 userID가 존재하면
        ssid = session.get('userID')    # 세션을 가져옴
        return render_template('index.html', ssid=ssid)
    else:
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
    if 'userID' in session:     # session에 userID가 존재하면
        ssid = session.get('userID')    # 세션을 가져옴
        return render_template('member_list.html', ssid=ssid, rs=rs)
    else:
        return render_template('member_list.html')


@app.route('/member_view/<string:id>/')
def member_view(id):    # mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % id
    cur.execute(sql)
    rs = cur.fetchone()     # 해당 1개의 자료를 반환
    conn.close()
    if 'userID' in session:     # session에 userID가 존재하면
        ssid = session.get('userID')    # 세션을 가져옴
        return render_template('member_view.html', ssid=ssid, rs=rs)
    else:
        return render_template('member_view.html', rs=rs)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        # date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member(mid, passwd, name, age) VALUES ('%s', '%s', '%s', '%s')" \
              % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()

        # 가입 후 자동 로그인
        sql = "SELECT * FROM member WHERE mid = '%s' " % id
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()

        if rs:
            session['userID'] = id
            # 자동 로그인 시 세션 발급 필수
            return redirect(url_for('member_list'))
        return redirect(url_for('member_list'))  # url 경로로 이동
    else:
        return render_template('register.html')  # GET 방식


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # 자료 전달 받음
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if rs:
            session['userID'] = id  # 세션 발급
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/logout/')
def logout():
    # session.pop('userID')   # userID 세션 삭제
    # 전체의 세션 삭제
    session.clear()
    return redirect(url_for('index'))


@app.route('/member_del/<string:id>/')  # 삭제 url
def member_del(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('member_list'))


@app.route('/member_edit/<string:id>/', methods=['GET', 'POST'])  # 수정 url
def member_edit(id):
    if request.method == "POST":
        # 자료를 넘겨 받음
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name = '%s', age = '%s', regDate = '%s' " \
            "WHERE mid = '%s' " % (pwd, name, age, date, id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))  # member_view 해당 id로 이동
    else:
        # 회원 자료 가져오기
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if 'userID' in session:
            ssid = session.get('userID')
            return render_template('member_edit.html', rs=rs, ssid=ssid)
        else:
            return render_template('member_edit.html')


app.run(debug=True)

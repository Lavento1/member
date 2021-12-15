from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "rlawlsxo"  # 암호키 설정


def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn


@app.route('/')  # 127.0.0.1:5000
def index():
    if 'userID' in session:  # session에 userID가 존재하면
        ssid = session.get('userID')  # 세션을 가져옴
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
    return render_template('member_list.html', rs=rs)


@app.route('/member_view/<string:id>/')
def member_view(id):  # mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % id
    cur.execute(sql)
    rs = cur.fetchone()  # 해당 1개의 자료를 반환
    conn.close()
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
        sql = "INSERT INTO member(mid, passwd, name, age) VALUES ('%s', '%s', '%s', %s)" \
              % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()

        # 가입 후 자동 로그인
        sql = "SELECT * FROM member WHERE mid = '%s' " % id
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()

        if rs:
            session['userID'] = rs[0]
            session['userName'] = rs[2] # 이름 세션 발급
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
            session['userID'] = rs[0]
            session['userName'] = rs[2]
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

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name = '%s', age = %s " \
              "WHERE mid = '%s' " % (pwd, name, age, id)
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
        return render_template('member_edit.html', rs=rs)


# 게시판 목록
@app.route('/board_list/')
def board_list():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('board_list.html', rs=rs)


# 게시글 작성
@app.route('/writing/', methods=['GET', 'POST'])
def writing():
    if request.method == "POST":
        # 자료 전달받음
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userName')  # 글쓴이 - 로그인한 이름(세션 권한 존재)

        # db에 글 추가
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO board(title, content, mid) VALUES ('%s', '%s', '%s') " % \
              (title, content, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()

        return redirect(url_for('board_list'))
    else:
        return render_template('writing.html')


# 게시글 상세보기
@app.route('/board_view/<int:bno>/')
def board_view(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = %s" % bno
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('board_view.html', rs=rs)


# 게시글 삭제
@app.route('/board_del/<int:bno>/')
def board_del(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = %s" % bno
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('board_list'))


@app.route('/board_edit/<int:bno>/', methods=['GET', 'POST'])
def board_edit(bno):
    if request.method == "POST":
        # 자료 전달 받음
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userName')

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE board SET title = '%s', content = '%s', mid = '%s' " \
              "WHERE bno = '%s' " % (title, content, mid, bno)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('board_view', bno=bno))
    else:   # board_view와 동일
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM board WHERE bno = %s" % bno
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('board_edit.html', rs=rs)


app.run(debug=True)

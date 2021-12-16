import sqlite3


def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn


def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
        CREATE TABLE member(
            mid CHAR(5) PRIMARY KEY,
            passwd CHAR(8) NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            regDate TIMESTAMP DATE DEFAULT (datetime('now', 'localtime'))
        );
    """

    cur.execute(sql)
    conn.commit()
    print("member 테이블 생성 완료")
    conn.close()


def drop_table():
    conn = getconn()
    cur = conn.cursor()
    sql = "DROP TABLE member"
    cur.execute(sql)
    conn.commit()
    conn.close()


def insert_member(mid, passwd, name, age):
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO member(mid, passwd, name, age) VALUES(?, ?, ?, ?)"
    cur.execute(sql, (mid, passwd, name, age))
    conn.commit()
    print("멤버 추가")
    conn.close()


def select_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()
    print(rs)
    for i in rs:
        print(i[0])
    conn.close()


def delete_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member"
    cur.execute(sql)
    conn.commit()
    conn.close()


create_table()
# drop_table()
# insert_member('cloud', 'm123456@', '구름', 100)
# delete_member()
# select_member()

import json
import threading
import pymysql
from flask import Flask, request

app = Flask(__name__)




conn = "123"
lock = threading.Lock()

@app.route("/api/Login", methods=['POST'])
def login():
    username = request.json['username']
    pwd = request.json['pwd']
    try:
        globals()['conn'].close
    except:
        pass
    try:
        globals()['conn'] = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='wyh77598.',
            database='sjdDB',
            charset='utf8'
        )
        print(1)
        sql="call check_user_account('" + username + "','" + pwd + "');"
        cursor = conn.cursor()
        cursor.execute(sql)
        print(2)
        str = cursor.fetchall()
        jsonResult = []
        for row in str:
            pusername = row[1]
            puid = row[0]
            userInfo = {}
            userInfo['username'] = pusername
            userInfo['uid'] = puid
            jsonResult.append(userInfo)
        if len(jsonResult) == 0:
            return "login failed", 501
        return  json.dumps(jsonResult,ensure_ascii=False), 200
    except:
        print('cnm')
        return 'login failed', 501

@app.route("/api/Register", methods=['POST'])
def register():
    username = request.json['username']
    pwd = request.json['pwd']
    try:
        globals()['conn'].close
    except:
        pass
    try:
        print(2)
        globals()['conn'] = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='wyh77598.',
            database='sjdDB',
            charset='utf8'
        )
        print(1)
        sql="call add_user_account('{}','{}');".format(username, pwd)
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print(3)
        sql2 = "call check_user_account('{}','{}');".format(username, pwd)
        cursor.execute(sql2)

        str = cursor.fetchall()
        for row in str:
            if row[1] == username:
                return 'register succeed', 200
    except:
        return 'register failed', 501


@app.route("/api/CoachTest", methods=['POST'])
def coachTest() :
    name = request.json['name']
    gender = request.json['gender']
    direction = request.json['direction']
    tel = request.json['tel']
    age = request.json['age']
    try:
        globals()['conn'].close
    except:
        pass
    try:
        print(2)
        globals()['conn'] = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='wyh77598.',
            database='sjdDB',
            charset='utf8'
        )
        sql = "call add_coach_list('{}','{}','{}','{}','{}');".format(name, gender, direction, tel, age)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        sql2 = "call check_coach_name('{}');".format(name)
        cursor.execute(sql2)
        str = cursor.fetchall()
        if len(str) >= 0:
            return 'register succeed', 200

    except:
        return 'register failed', 501

@app.route("/api/CoachList", methods=['POST'])
def getCoachList() :
    offset = request.json['params']['offset']
    limit = request.json['params']['limit']
    # print('offset:' + str(offset))
    # print('limit:' + str(limit))
    try:
        globals()['conn'].close
    except:
        pass
    try:
        globals()['conn'] = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='wyh77598.',
            database='sjdDB',
            charset='utf8'
        )
        sql = "select * from coach_list limit {},{}".format(offset, limit)
        cursor = conn.cursor()
        cursor.execute(sql)
        sstr = cursor.fetchall()
        strLen = len(sstr)
        # print(strLen)
        jsonResult = []
        for row in sstr:
            pname = row[0]
            puid = row[1]
            pgender = row[2]
            pdirection = row[3]
            ptel = row[4]
            age = row[5]
            coachInfo = {}
            coachInfo['name'] = pname
            coachInfo['uid'] = puid
            coachInfo['gender'] = pgender
            coachInfo['direction'] = pdirection
            coachInfo['tel'] = ptel
            coachInfo['age'] = age
            jsonResult.append(coachInfo)
        # for i in range(offset, offset + limit):
        #     print(i)
        #     if i <= strLen - 1:
        #         pname = sstr[i][0]
        #         puid = sstr[i][1]
        #         pgender = sstr[i][2]
        #         pdirection = sstr[i][3]
        #         ptel = sstr[i][4]
        #         age = sstr[i][5]
        #         coachInfo = {}
        #         coachInfo['name'] = pname
        #         coachInfo['uid'] = puid
        #         coachInfo['gender'] = pgender
        #         coachInfo['direction'] = pdirection
        #         coachInfo['tel'] = ptel
        #         coachInfo['age'] = age
        #         jsonResult.append(coachInfo)
        if len(jsonResult) == 0:
            return "没有数据"
        return json.dumps(jsonResult, ensure_ascii=False)
    except:
        print('cnm')
        return '查询失败', 501

@app.route("/api/GetItemsNum", methods=['POST'])
def getItemsNum() :
    try:
        globals()['conn'].close
    except:
        pass
    try:
        globals()['conn'] = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='wyh77598.',
            database='sjdDB',
            charset='utf8'
        )
        sql = "select count(*) from coach_list;"
        cursor = conn.cursor()
        cursor.execute(sql)
        sstr = cursor.fetchall()
        print(str(sstr[0][0]))
        return str(sstr[0][0]), 200
    except:
        print('cnm')
        return '查询失败', 501












if __name__ == '__main__':
    app.run(debug=True,threaded=False)

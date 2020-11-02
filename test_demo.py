#coding:utf-8
from flask import Flask, request, Response
import json
import MySQLdb
from flask import make_response

app = Flask(__name__)

_db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8")
_cursor = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user',methods=['GET'])
def user():
    #sql = '''SELECT id,name,birthday FROM users1 LIMIT 10'''
    sql = '''SELECT * FROM users LIMIT 10'''
    _cursor = _db.cursor()
    try:
        _cursor.execute(sql)
        row_headers = [x[0] for x in _cursor.description]
        results = _cursor.fetchall()
        print('results:',results)
        #查询结果集转换为list
        new_list = []
        for x in results:
            new_list.append(list(x))
        #日期转换为字符串
        for i in new_list:
            i[2] = str(i[2])
        #组装josn
        json_data = []
        #for result in new_list:     #演示：new_list为已经将时间转为字符串的list，results为原始时间元组,new_list->results
        for result in new_list:
            json_data.append(dict(zip(row_headers, result)))
        print('json_data:',json_data)
    except:
        _db.rollback()
    _cursor.close()
    rst = make_response(json.dumps(json_data))
    rst.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
    return rst
    #return json.dumps(json_data)

@app.route('/posts',methods=['POST'])
def posts():
    user_id = request.form.get('id')
    user_name = request.form.get('name')
    user_birthday = request.form.get('birthday')
    print(user_id,user_name,user_birthday)
    try:
        #演示：user_id不做转换，int(user_id)->user_id / user_id输入非整型
        sql = "insert into users(id,name,birthday) values  ('%d', '%s', '%s')" % (int(user_id), user_name, user_birthday)
        print("提交数据库的sql为:",sql)
        #sql = "insert into users (id,name,birthday) values  ('%d', '%s', '%s')" % (user_id, user_name, user_birthday)
        ret = _db.cursor().execute(sql)
        return u'数据写入成功：'+user_id+'，'+ user_name +'，' + user_birthday
    except MySQLdb.IntegrityError:
        pass
    return u'数据写入成功！'    #演示：id已存在/id超过10位

if __name__ == '__main__':
	app.run()

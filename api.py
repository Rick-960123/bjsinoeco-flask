from flask import Flask, jsonify
from werkzeug.utils import secure_filename
from flask import request
from flask_cors import CORS
import time, os, random
import mysql.connector
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['JSON_AS_ASCII'] = False
i, y, filename, filePath = 0, 0, ['', '', '', '', ''], ['', '', '', '', '']
def createdb(value):
    conn = mysql.connector.connect(user='root', password='Show78952@', database='files', use_unicode=True)
    cursor = conn.cursor()
    if len(value) == 15:
        print('123')
        cursor.execute('insert into file (id,title,content,url1,url2,url3,url4,url5,create_time,date,filename, filename1,filename2, filename3, filename4) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', value)
        conn.commit()
    else:
        cursor.execute('insert into file1 (id,name,type,company,date,create_time,deletebit ) values (%s,%s,%s,%s,%s,%s,%s)',value)
        conn.commit()
    cursor.close()
def selectdb(val):
    conn = mysql.connector.connect(user='root', password='Show78952@', database='files', use_unicode=True)
    cursor = conn.cursor()
    if val == 0:
        cursor.execute('select * from file')
        abc = cursor.fetchall()
        cursor.close()
        return abc
    if val == 1:
        cursor.execute('select * from file1')
        abc = cursor.fetchall()
        cursor.close()
        return abc
def edit_db(value):
    conn = mysql.connector.connect(user='root', password='Show78952@', database='files', use_unicode=True)
    cursor = conn.cursor()
    print(value)
    if 'title' in value:
        cursor.execute("update file set deletebit=%(deletebit)s where title=%(title)s and date=%(date)s", value)
    else:
        cursor.execute("update file1 set deletebit=%(deletebit)s where name=%(name)s and date=%(date)s", value)
    conn.commit()
    cursor.close()
@app.route('/getdata', methods=['GET'])
def getdata():
    a = request.args.get('data')
    if a == "file":
        val = 0
        abc = selectdb(val)
        return jsonify({
             "data": [d for d in abc],
                        }), 200
    if a == "file1":
        val = 1
        abc = selectdb(val)
        return jsonify({
             "data": [d for d in abc],
                        }), 200
@app.route('/upload', methods=['POST'])
def upload():
    global filename, filePath
    file = request.files.getlist('file')
    y = 0
    print(file)
    filename,filePath=['', '', '', '', ''],['', '', '', '', '']
    name = str(random.randint(0, 99))
    for f in file:
        creattime = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        filename2 = secure_filename(f.filename)
        if len(filename2) < 5:
            filename1 = creattime+name+'.'+filename2
        elif len(filename2) > 15:
            filename1 = filename2
        else:
            filename1 = creattime+name+filename2
        basepath = os.path.dirname(__file__)
        print(filename1)
        upload_path = os.path.join(basepath, '../tomcat/webapps/dist/static', filename1)
        f.save(upload_path)
        filename[y] = f.filename
        filePath[y] = upload_path
        print(filePath)
        y = y+1
    return jsonify({"res": True}), 200

@app.route('/update', methods=['POST'])
def update():
    print(request.form)
    if request.form['data'] == 'file':
        value = {'date':0,'title':0,'deletebit':0 }
        value['date'] = request.form['date']
        value['title'] = request.form['title']
        value['deletebit'] = request.form['deletebit']
        print(value)
        edit_db(value)
        return jsonify({
            "res": True
        }), 200
    if request.form['data'] == 'file1':
        value = {'date':0,
                 'name': 0,
                 'deletebit':0
                 }
        value['date'] = request.form['date']
        value['name'] = request.form['name']
        value['deletebit'] = request.form['deletebit']
        print(value)
        edit_db(value)
        return jsonify({
            "res": True
        }), 200

@app.route('/signin', methods=['POST'])
def signin():
    if 'title'in request.form:
        value = ['','','','','','','','','','','','','','','']
        global i,y ,filename, filePath
        i = i+1
        creattime = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        value[0] = i
        value[1] = request.form['title']
        value[2] = request.form['content']
        value[3] = filePath[0]
        value[4] = filePath[1]
        value[5] = filePath[2]
        value[6] = filePath[3]
        value[7] = filePath[4]
        value[8] = creattime
        value[9] = request.form['date']
        value[10] = filename[0]
        value[11] = filename[1]
        value[12] = filename[2]
        value[13] = filename[3]
        value[14] = filename[4]
        print(value)
        createdb(value)
        filePath= ['','','','','']
        filename= ['','','','','']
        return jsonify({
            "res": True
        }), 200
    if 'company' in request.form:
        value = ['', '', '', '', '', '','']
        y = y + 1
        creattime = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        value[0] = y
        value[1] = request.form['name']
        value[2] = request.form['type']
        value[3] = request.form['company']
        value[4] = request.form['date']
        value[5] = creattime
        value[6] = ''
        print(value)
        createdb(value)
        return jsonify({
            "res": True
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
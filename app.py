##############################################################################################################
##############################################################################################################
# Example of Flask jsonify
# Source: https://www.fullstackpython.com/flask-json-jsonify-examples.html
# Example of Flask Request
# Source: https://www.programcreek.com/python/example/60711/flask.request.data
# Example of Flask Redirect
# Source: https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
# Example of Flask Templates
# Source: https://flask.palletsprojects.com/en/2.0.x/tutorial/templates/
# Werkzeug Documents
# Source: https://werkzeug.palletsprojects.com/en/2.0.x/
# Documents and Demo of transcription
# Demo Source: https://xfyun-doc.cn-bj.ufileos.com/1564736425808301/weblfasr_python3_demo.zip
# Document Source: https://www.xfyun.cn/services/lfasr
##############################################################################################################
##############################################################################################################


import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import jsonify, request, redirect, render_template, Response
from utilities.transcription.generate_transcription import generate
from utilities.db import NewSession, User, Group, Meeting, Roles
from utilities.CONFIG import Database
from sqlalchemy import exists
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from flask_cors import CORS
from init import create_app
from utilities.CONFIG import DefaultConfig, AppRun

db = Database.NAME
app = create_app(__name__)
CORS(app, supports_credentials=True)
secrete_key = DefaultConfig.SECRET_KEY
LOGINSESSION = dict()
session = NewSession()


# user login
@app.route('/login/')
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    userinfo = {}
    sql = f"select * from {db}.user where name= '{username}' and password='{password}';"
    result = session.execute(sql)
    row = result.fetchall()
    if not result.rowcount:
        msg = 'Invalid username or password.'
        status = 0
        return jsonify({'msg': msg, 'status': status})
    msg = 'Login successfully.'
    status = True
    for r in row:
        id = r[0]
    LOGINSESSION['id'] = hash(username)
    LOGINSESSION['username'] = hash(id)
    payload = {
        "id": LOGINSESSION['id'],
        "name": LOGINSESSION['username'],
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    # Generate Token
    # Source: https://pyjwt.readthedocs.io/en/latest/
    token = jwt.encode(payload, key=secrete_key, algorithm='HS256')
    for r in row:
        userinfo = {}
        userinfo['userid'] = r[0]
        userinfo['name'] = r[1]
        userinfo['emial'] = r[3]
        userinfo['gender'] = r[4]
        userinfo['dob'] = r[5]
        userinfo['address'] = r[6]
    return jsonify({'msg': msg, 'status': status, 'userinfo': userinfo, 'LOGINSESSION': LOGINSESSION, 'token': token})


@app.route('/register/')
def register():
    name = request.values.get('name')
    password = request.values.get('password')
    email = request.values.get('email')
    gender = request.values.get('gender')
    dob = request.values.get('dob')
    address = request.values.get('address')
    if name is None or password is None or email is None:
        msg = 'User name, password or email cannot be empty.'
        status = False
        return jsonify({"msg": msg, "status": status})
    if gender is None:
        gender = ''
    if dob is None:
        dob = datetime.now()
    if address is None:
        address = 'None'
    if session.query(exists().where(User.name == name)).scalar():
        msg = 'Existed Username.'
        status = False
        return jsonify({"msg": msg, "status": status})
    if session.query(exists().where(User.email == email)).scalar():
        msg = 'Existed Email Address.'
        status = False
        return jsonify({"msg": msg, "status": status})
    try:
        user = User(name=name, password=password, email=email, gender=gender, dob=dob, address=address)
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    sql = f"select * from {db}.user where name='{name}';"
    result = session.execute(sql)
    users_obj = result.fetchall()
    users = list()
    for group in users_obj:
        user = dict()
        user['id'] = group[0]
        user['name'] = group[1]
        user['email'] = group[3]
        user['gender'] = group[4]
        user['dob'] = group[5]
        user['address'] = group[6]
        users.append(user)
    msg = 'Create account successfully.'
    status = True
    return jsonify({"msg": msg, "status": status, 'users': users})


@app.route('/logout/')
def logout():
    LOGINSESSION['id'] = ''
    LOGINSESSION['username'] = ''
    msg = 'Logout successfully.'
    status = True
    return jsonify({'msg': msg, 'status': status})


# Modify User's Password
@app.route('/modify/')
def modify():
    userid = request.values.get('userid')
    username = request.values.get('username')
    newpassword = request.values.get('newpassword')
    token = request.headers.get('token')
    status = False
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again.'
        status = False
        return jsonify({'msg': msg, 'status': status})
    sql = f"select * from {db}.user where name='{username}' and id='{userid}';"
    result = session.execute(sql)
    if result.rowcount != 0:
        sql = f"update {db}.user set password='{newpassword}' where name='{username}' and id='{userid}';"
        try:
            session.execute(sql)
            session.commit()
            msg = 'Update password successfully.'
            status = True
        except Exception as e:
            session.rollback()
            msg = str(e)
            status = False
    return jsonify({'msg': msg, 'status': status})


# Change User's Information
@app.route('/modifyinfo/')
def modifyinfo():
    name = request.values.get('username')
    password = request.values.get('password')
    gender = request.values.get('gender')
    dob = request.values.get('dob')
    address = request.values.get('address')
    userid = request.values.get('userid')
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again'
        status = False
        return jsonify({'msg': msg, 'status': status})
    try:
        user_obj = session.query(User).filter(User.id == userid).update(
            {"name": name, "password": password, "gender": gender, "dob": dob,
             "address": address})
        session.commit()
        if user_obj == 1:
            msg = 'User information changed successfully.'
            status = True
        else:
            msg = 'User does not exist.'
            status = False
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
    return jsonify({'status': status, "msg": msg})


# create group
@app.route('/addgroup/')
def addgroup():
    groupin = {}
    name = request.values.get('gropuname')
    description = request.values.get('description')
    originator = request.values.get('originator')
    createtime = datetime.now()
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again'
        status = False
        return jsonify({'msg': msg, 'status': status})
    if name is None:
        sql = "select max(id)+1 from {db}.group;"
        result = session.execute(sql).fetchall()
        name = result[0][0]
    if description is None:
        description = 'None'
    if originator is None:
        sql = "select min(id) from {db}.user;"
        result = session.execute(sql).fetchall()
        originator = result[0][0]
    if session.query(exists().where(Group.name == name)).scalar():
        msg = 'Existed Group.'
        status = False
        return jsonify({"msg": msg, "status": status, 'groupinfo': groupin})
    try:
        group = Group(name=name, createtime=createtime, description=description, originator=originator)
        session.add(group)
        session.commit()
        msg = 'Create group successfully.'
        status = True
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    sql = f"select * from {db}.group where originator='{originator}';"
    result = session.execute(sql)
    groups = []
    for group in result.fetchall():
        groupin = {}
        groupin['id'] = group[0]
        groupin['name'] = group[1]
        groupin['createtime'] = group[2]
        groupin['description'] = group[3]
        groupin['originator'] = group[4]
        groups.append(groupin)
    return jsonify({"msg": msg, "status": status, 'groupinfo': groupin})


# Modify group information
@app.route('/modifygroups/')
def modifygroups():
    name = request.values.get('gropuname')
    description = request.values.get('description')
    originator = request.values.get('originator')
    id = request.values.get('id')
    createtime = datetime.now()
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again'
        status = False
        return jsonify({'msg': msg, 'status': status})
    try:
        group_obj = session.query(Group).filter(Group.id == id).update(
            {"name": name, "createtime": createtime, "description": description, "originator": originator
             })
        session.commit()
        if group_obj == 1:
            msg = 'Group information updated successfully.'
            status = True
        else:
            msg = 'Group does not exist.'
            status = False
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    return jsonify({"msg": msg, "status": status})


# add group member
@app.route('/addgroupspeople/')
def addgroupspeople():
    user_id = request.values.get('user_id')
    group_id = request.values.get('group_id')
    role = request.values.get('role')
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again'
        status = False
        return jsonify({'msg': msg, 'status': status})
    if user_id is None or group_id is None:
        msg = 'Failed to add member, user_id,group_ID cannot be empty.'
        status = False
        return jsonify({"msg": msg, "status": status})
    if role is None:
        role = 'Ordinary'
    rows = session.query(Roles).filter_by(user_id=user_id, group_id=group_id).all()
    if len(rows) > 0:
        msg = 'Fail to add group member.'
        status = False
    else:
        try:
            role = Roles(user_id=user_id, group_id=group_id, role=role)
            session.add(role)
            session.commit()
            msg = 'Add group member successfully.'
            status = True
        except Exception as e:
            session.rollback()
            msg = str(e)
            status = False
            return jsonify({"msg": msg, "status": status})
    return jsonify({"msg": msg, "status": status})


# remove group member
@app.route('/deletegroupspeople/')
def deletegroupspeople():
    session2 = NewSession()
    user_id = request.values.get('user_id')
    group_id = request.values.get('group_id')
    role = request.values.get('role')
    if user_id is None or group_id is None:
        msg = 'Failed to add member, user_ id,group_ ID cannot be empty'
        status = False
        return jsonify({"msg": msg, "status": status})
    session2.query(Roles).filter_by(user_id=user_id,group_id=group_id).delete()
    return jsonify({"msg": "ok", "status": "ok"})


# get all members in the group
@app.route('/getgroupspeople/')
def getgroupspeople():
    session2 = NewSession()
    group_id = request.values.get('group_id')
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again'
        status = False
        return jsonify({'msg': msg, 'status': status})
    groupspeople = []
    sql = f"select * from {db}.roles a inner join {db}.user b on a.user_id=b.id where group_id='{group_id}';"
    result = session2.execute(sql)
    for users in result.fetchall():
        user = {}
        user['id'] = users[0]
        user['user_id'] = users[1]
        user['group_id'] = users[2]
        user['role'] = users[3]
        user['name'] = users[5]
        user['email'] = users[6]
        user['gender'] = users[7]
        user['dob'] = users[8]
        user['address'] = users[9]
        groupspeople.append(user)
    if len(groupspeople) > 0:
        msg = 'Get group members successfully.'
        status = True
    else:
        msg = 'Failed to get group members.'
        status = False
    return jsonify({"msg": msg, "status": status, 'groupspeople': groupspeople})


# get user information
@app.route('/getuser/')
def getuser():
    users = []
    session2 = NewSession()
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    if data['id'] != LOGINSESSION['id']:
        msg = 'Verification failed, please log in again.'
        status = False
        return jsonify({'msg': msg, 'status': status})
    sql = f"select * from {db}.user;"
    try:
        result = session2.execute(sql)
        users_obj = result.fetchall()
        for group in list(users_obj):
            user = {}
            user['id'] = group[0]
            user['name'] = group[1]
            user['email'] = group[3]
            user['gender'] = group[4]
            user['dob'] = group[5]
            user['address'] = group[6]
            users.append(user)
        msg = 'Get user information successfully.'
        status = True
    except Exception as e:
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    return jsonify({"msg": msg, "status": status, 'users': users})


# get group information
@app.route('/getgroupinfo/')
def getgroupinfo():
    group_infos = []
    session2 = NewSession()
    originator = request.values.get('user_id')
    if originator is None:
        msg = 'The current user ID was not obtained'
        status = False
        return jsonify({'msg': msg, 'status': status})
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    try:
        if data['id'] != LOGINSESSION['id']:
            msg = 'Verification failed, please log in again'
            status = False
            return jsonify({'msg': msg, 'status': status})
    except Exception as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    sql = f"select * from {db}.group where originator='{originator}';"
    sql2 = f"select * from {db}.group where id in  (SELECT group_id from {db}.roles where user_id={originator});"
    try:
        result = session2.execute(sql)
        groupinfo_obj = result.fetchall()
        for group in list(groupinfo_obj):
            group_info = {}
            group_info['id'] = group[0]
            group_info['name'] = group[1]
            group_info['createtime'] = group[2]
            group_info['description'] = group[3]
            group_info['originator'] = group[4]
            group_infos.append(group_info)
        result = session2.execute(sql2)
        groupinfo_obj = result.fetchall()
        for group in list(groupinfo_obj):
            group_info = {}
            group_info['id'] = group[0]
            group_info['name'] = group[1]
            group_info['createtime'] = group[2]
            group_info['description'] = group[3]
            group_info['originator'] = group[4]
            group_infos.append(group_info)
        msg = 'Successfully obtained all group information'
        status = True
    except Exception as e:
        session2.rollback()
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    return jsonify({"msg": msg, "status": status, 'group_infos': group_infos})


# get meeting information
@app.route('/getmeetinginfo/')
def getmeetinginfo():
    metting_infos = []
    group_id = request.values.get('group_id')
    if group_id is None:
        msg = 'The current group ID was not obtained'
        status = False
        return jsonify({'msg': msg, 'status': status})
    token = request.headers.get('token')
    try:
        data = jwt.decode(token, key=secrete_key, algorithms='HS256')
    except PyJWTError as e:
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    try:
        if data['id'] != LOGINSESSION['id']:
            msg = 'Validation failed, please login again.'
            status = False
            return jsonify({'msg': msg, 'status': status})
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
        return jsonify({'msg': msg, 'status': status})
    sql = f"select * from {db}.meeting where group_id='{group_id}';"
    try:
        result = session.execute(sql)
        groupinfo_obj = result.fetchall()
        for group in list(groupinfo_obj):
            group_info = {}
            group_info['id'] = group[0]
            group_info['name'] = group[1]
            group_info['starttime'] = group[2]
            group_info['endtime'] = group[3]
            group_info['group_id'] = group[4]
            metting_infos.append(group_info)
        msg = 'Successfully retrieved all group information.'
        status = True
    except Exception as e:
        session.rollback()
        msg = str(e)
        status = False
        return jsonify({"msg": msg, "status": status})
    return jsonify({"msg": msg, "status": status, 'metting_infos': metting_infos})


# upload files
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        gid = request.values.get('gid')
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        if not os.path.isdir(os.path.join(basepath, 'static/uploads', gid)):
            os.mkdir(os.path.join(basepath, 'static/uploads', gid))
        upload_path = os.path.join(basepath, 'static', 'uploads', gid,
                                   secure_filename(f.filename))
        f.save(upload_path)
        return redirect('http://127.0.0.1:5000/metting2.html')
    return render_template('upload.html')


# get all files uploaded by the group members
@app.route('/filelist', methods=['POST', 'GET'])
def filelist():
    gid = request.values.get('gid')
    # path of current file
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'static/uploads', gid)
    if os.path.isdir(os.path.join(upload_path)) == False:
        return jsonify({'msg': [], 'status': 1})
    for root, dirs, files in os.walk(upload_path, topdown=False):
        for name in files:
            print(os.path.join(root, name))
    return jsonify({'msg': files, 'status': 1})


# get meeting information
@app.route('/getmeet2', methods=['POST', 'GET'])
def getmeet2():
    session2 = NewSession()
    gid = request.values.get('gid')
    sql = f"select * from {db}.meeting where group_id='{gid}';"
    result = session2.execute(sql)
    row = result.fetchall()
    if result.rowcount == 0:
        msg = 'Fail to get info of meeting.'
        return jsonify({'msg': msg, 'status': False})
    if result.rowcount >= 1:
        msg = {}
        msg['id'] = row[0][0]
        msg['name'] = row[0][1]
        msg['starttime'] = row[0][2]
        msg['endtime'] = row[0][3]
        msg['group_id'] = row[0][4]
    return jsonify({'msg': msg, 'status': True})


# update meeting information
@app.route('/updatemeet2', methods=['POST', 'GET'])
def updatemeet2():
    gid = request.values.get('gid')
    starttime = request.values.get('starttime')
    endtime = request.values.get('endtime')
    name = request.values.get('name')
    sql = f"select * from {db}.meeting where group_id= '{gid}';"
    result = session.execute(sql)
    if result.rowcount == 0:
        met = Meeting(name=name, starttime=starttime, endtime=endtime, group_id=gid)
        session.add(met)
        session.commit()
    if result.rowcount > 0:
        session.query(Meeting).filter(Meeting.group_id == gid).update(
            {"endtime": endtime, "starttime": starttime, "name": name
             })
        session.commit()
    return jsonify({'msg': "update success", 'status': 1})


# generate transcription for mp4
@app.route('/mp42text', methods=['POST', 'GET'])
def mp42text():
    gid = request.values.get('gid')
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'static/uploads', gid)
    if os.path.isdir(os.path.join(upload_path)) == False:
        return jsonify({'msg': [], 'status': 1})
    for root, dirs, files in os.walk(upload_path, topdown=False):
        for name in files:
            if 'mp4' in name:
                generate(upload_path + "/" + name)
    return jsonify({'msg': files, 'status': 1})


@app.route('/goto', methods=['POST', 'GET'])
def goto():
    return redirect('http://127.0.0.1:5000/upload.html')


# download files
@app.route('/get_file2/')
def get_file2():
    filename = request.values.get('filename')
    gid = request.values.get('gid')
    def send_file2():
        filepath = os.path.dirname(__file__)
        f = '/static/uploads/'+gid+'/'+filename
        store_path = filepath+f
        store_path = Path(store_path)
        if not store_path.exists():
            msg = 'File does not exist.'
            status = False
            return jsonify({"msg": msg, "status": status})
        with open(store_path, 'rb') as targetfile:
            while 1:
                # Read 20MB for each time
                data = targetfile.read(20 * 1024 * 1024)
                if not data:
                    break
                yield data
    response = Response(send_file2(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = f'attachment; filename={filename}'
    return response


if __name__ == '__main__':
    app.run(host=AppRun.host, port=AppRun.port, debug=AppRun.debug)

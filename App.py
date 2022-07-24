import flask
from flask import Flask, render_template, request,flash,redirect,url_for,session
import os
import sqlite3
import re

app = Flask(__name__)
app.secret_key="123"

app.config['UPLOAD_FOLDER']="static\images\certificates"
database =r".\database\Users.db"
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    database =r".\database\Users.db"
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            cursor.execute('select * from user_infos where USER_ID= ?', (account['id'],))
            data=cursor.fetchone()
            con.close()
            return render_template("index.html",account=account,data=data,msg = msg)
        else:
            msg = 'Incorrect username / password !'
          
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    database =r".\database\Users.db"
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email) VALUES ( ?, ?, ?)', (username, password, email))
            con.commit()
            msg = 'You have successfully registered ! Wait...'
            return render_template('redirect.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
@app.route('/redirect')
def redirecttologin():
    return render_template('redirect.html')

@app.route("/certificate",methods=['GET','POST'])
def upload():
    database =r".\database\Users.db"
    userid=session['id']
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select * from CERTIFICATE where USER_ID= ?', (userid,))
    data = cur.fetchall()
    cur.execute('SELECT * FROM accounts WHERE username = ?', (session['username'],))
    account = cur.fetchone()
    con.close()

    if request.method=='POST':
        upload_image=request.files['upload_image']
        description=request.form['Description'] 
        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            con=sqlite3.connect(database)
            cur=con.cursor()
            cur.execute("insert into CERTIFICATE(USER_ID,IMAGE_NAME,DESCRAPTION)values(?,?,?)",(userid,upload_image.filename,description,))
            con.commit()
            flash("File Upload Successfully","success")

            con = sqlite3.connect(database)
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute('select * from CERTIFICATE where USER_ID= ?', (userid,))
            data=cur.fetchall()
            con.close()
            return render_template("certificate.html",account=account,data=data)
    return render_template("certificate.html",account=account,data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    database =r".\database\Users.db"
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute("delete from CERTIFICATE where id=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
        con.close()

@app.route("/editprofile",methods=['GET','POST'])
def editprofile():
    database =r".\database\Users.db"
    userid=session['id']
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select * from user_infos where USER_ID= ?', (userid,))
    data = cur.fetchone()
    con.close()

    if request.method=='POST':
        firstname=request.form['firstname']
        lastname =request.form['lastname']
        mobilenumber=request.form['mobilenumber']
        addressline1=request.form['addressline1']
        addressline2=request.form['addressline2']
        postcode=request.form['postcode']
        state=request.form['state']
        area=request.form['area']
        education=request.form['education']
        country=request.form['country']
        Experience=request.form['Experience']
        additional_details=request.form['additional_details']
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute("insert into user_infos(user_id,firstname,lastname,mobile_number,addressline1,addressline2,postcode,state,area,education,country,Experience,additional_details) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(userid,firstname,lastname,mobilenumber,addressline1,addressline2,postcode,state,area,education,country,Experience,additional_details,))
        con.commit()
        flash("File Upload Successfully","success")
        con = sqlite3.connect(database)
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute('select * from user_infos where USER_ID= ?', (userid,))
        data=cur.fetchall()
        con.close()
        return render_template("editprofile.html",data=data)
    return render_template("editprofile.html",data=data)

@app.route("/index",methods=['GET','POST'])
def profile():
    database =r".\database\Users.db"
    userid=session['id']
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select * from user_infos where USER_ID= ?', (userid,))
    data = cur.fetchone()
    cur.execute('SELECT * FROM accounts WHERE username = ?', (session['username'],))
    account = cur.fetchone()

    if request.method=='POST':
        firstname=request.form['firstname']
        lastname =request.form['lastname']
        mobilenumber=request.form['mobilenumber']
        addressline1=request.form['addressline1']
        addressline2=request.form['addressline2']
        postcode=request.form['postcode']
        state=request.form['state']
        area=request.form['area']
        education=request.form['education']
        country=request.form['country']
        Experience=request.form['Experience']
        additional_details=request.form['additional_details']
        if data:
          cur.execute("update  user_infos set firstname=?,lastname=?,mobile_number=?,address_line1=?,address_line2=?,postcode=?,state=?,area=?,education=?,country=?,Experience=?,additional_details=? WHERE user_id = ?",(firstname,lastname,mobilenumber,addressline1,addressline2,postcode,state,area,education,country,Experience,additional_details,userid))
          con.commit()
        else :
          cur.execute("insert into user_infos(user_id,firstname,lastname,mobile_number,address_line1,address_line2,postcode,state,area,education,country,Experience,additional_details) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(userid,firstname,lastname,mobilenumber,addressline1,addressline2,postcode,state,area,education,country,Experience,additional_details,))
          con.commit()
        flash("Update Successfully","success")
        cur.execute('select * from user_infos where USER_ID= ?', (userid,))
        data=cur.fetchone()
        con.close()
        return render_template("index.html",account=account,data=data)
    return render_template("index.html",account=account,data=data)

if __name__ == '__main__':
    app.run(debug=True)
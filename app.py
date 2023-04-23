from flask import Flask,render_template,session,abort,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,emit
from function import gen_string,add_Message,add_user,form_connection,form_singup,get_Message,get_user,create_session
import datetime,time,os,json
app = Flask(__name__)
app.config['SECRET_KEY'] = "thisismysecretkey:M@zongdongmo2003Sentioergosum"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_LEFT_TIME'] = 10
socketio = SocketIO(app)
db = SQLAlchemy(app)
User_connected = 0
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    photo = db.Column(db.String(20),nullable=True)
    key  = db.Column(db.String(20),nullable=False)
class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(20),nullable=False)
    content = db.Column(db.String(200),nullable=False)
    data_url = db.Column(db.String(20),nullable=False)
    date = db.Column(db.String(10),default=time.strftime("%Y %m-%d %H:%M"))

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        u = get_user(User,username,password)
        if u == None:
            return render_template('index.html',error=['les identifiant sont incorrect'])
        else:
            session['username'] = u.username
            session['password'] = u.password
            global User_connected
            User_connected += 1
            return redirect("/home")
    return render_template("index.html")
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conf = request.form.get("conf")
        age = request.form.get("age")
        error = form_singup(username,age,password,conf)
        if len(error) == 0:
            u = User(username=username,password=password,age=age,key=gen_string(19))
            if add_user(db,u) == True:
                create_session(session,username,password)

                global User_connected
                User_connected += 1
                return redirect(url_for('home'))
            else:
                error.append("Nom d'utilisateur deja pris")
                return render_template("register.html",error=error)
        else:
            return render_template("register.html",error=error)
    return render_template("register.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/home")
def home():
    global User_connected
    if ("username" in session and "password" in session) and session['username'] != "" or session['password'] != "":
        u = User.query.filter_by(username=session["username"],password=session["password"]).first()
        profile = "data/"+str(u.key)+"profile.png"
        m = Message.query.order_by(Message.date).all()
        data = {'username':session['username'],'date':time.strftime("%D %H:%M:%S")
        ,'users':User_connected,'profile':profile}
        return render_template("home.html",data=data,message=m)
    else:
        return redirect(url_for('index'))
@app.route("/logout")
def logout():
    global User_connected
    User_connected -= 1
    session['username'] = ''
    session['password'] = ''
    return redirect('/')
@app.route("/home/profile")
def profile():
    return 'hello'
@app.errorhandler(404)
def error(err):
    return render_template('error.html')
@socketio.on('connect')
def connect():
    socketio.emit('client_connect',{'username':session['username'],'user_connected':User_connected})
@socketio.on('disconnect')
def disconnect():
    socketio.emit("client_disconnect",{'username':session['username'],'user_connected':User_connected})
    
@socketio.on('message')
def message(data):
    msg = {'msg':data['msg'],'username':session['username'],'date':time.strftime("%d %H:%M")}
    socketio.emit('new_message',msg)
    m = Message(author=session["username"],content=data["msg"],data_url=gen_string(20))
    db.session.add(m)
    db.session.commit()
@socketio.on("photo_profile")
def photo_profile(data):
    if data != None:
        u = User.query.filter_by(username=session["username"],password=session["password"]).first()
        if u != None:
            fic = open("data/"+str(u.key)+"/profile.png","wb+")
            fic.write(data["data"])
            fic.close()
if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=5004)

import string
from random import randint
import re
def gen_string(lenght):
    letter = string.ascii_letters+string.ascii_uppercase
    finale = ""
    for i  in range(lenght):
        index = randint(0,len(letter)-10)
        finale = finale+letter[index]
    return finale
def form_singup(username,age,password,conf):
    error = []
    if (username == None or username == '') or (len(username)<4 or len(username)>20):
        error.append("le nom")
    if len(password)<9-1 or password == None or (password != conf):
        error.append("mot de passe")
    if age == "" or age == None:
        error.append("age ")
    print(username,age,password,conf,sep=' ')
    print(error)
    return error
def form_connection(username,password):
    error = []
    if password == None or len(password)<7:
        error.append("le mot de passe")
    if username == None or (len(username)<4 or len(username)>20):
        error.append("identifiant incorrect")
    return error
def add_user(db,User):
    try:
       db.session.add(User)
       db.session.commit()
       return True
    except:
        return False
def get_user(User,username,password):
    u = User.query.filter_by(username=username,password=password).first()
    return u
def add_Message(db,Message):
    try:
        db.session.add(Message)
        db.session.commit()
        return True
    except:
        return False
def get_Message(Message):
    m = Message.limit(10).all()
    return m
def create_session(session,username,password):
    session['username'] = username
    session['password'] = password

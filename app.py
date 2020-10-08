from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')

app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student 테이블
class User(db.Model):
   __table_name__ = 'user'

   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50), nullable=False)
   email = db.Column(db.String(50), nullable=False)

   def __repr__(self):
      return f"<User('{self.id}', '{self.username}', '{self.email}')>"

# Assignment 테이블
class Assignment(db.Model):
   __table_name__ = 'assignment'

   id = db.Column(db.Integer, primary_key=True)
   assignment_title = db.Column(db.String(255), nullable=False)
   score = db.Column(db.Integer, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   def __repr__(self):
      return f"<Assignment('{self.id}', '{self.assignment_title}', '{self.score}')>"

@app.route('/')
def userList():
    return render_template('userList.html.j2', title='목록')

@app.route('/addUser')
def addUser():
   return render_template('addUSer.html.j2', title='추가')

@app.route('/userDetail')
def userDetail():
   return render_template('userDetail.html.j2', title='수강생 1')

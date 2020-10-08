from flask import Flask, render_template, request, url_for, redirect
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

   assignments = db.relationship('Assignment', backref='student', lazy=True)

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

# 유저 목록 Page (메인 페이지)
@app.route('/')
def userList():
   users = User.query.all()
   return render_template('userList.html.j2', title='목록', users=users)

# 유저 추가 Page
@app.route('/addUser')
def addUser():
   return render_template('addUSer.html.j2', title='추가')

# 유저 정보 Page
@app.route('/userDetail/<id>')
def userDetail(id):
   print('#### id #### : ', id)
   assignments = Assignment.query.all()
   print('##### assignment : ', assignments)

   return render_template('userDetail.html.j2', assignments=assignments)

# 유저 추가 엔드포인트
@app.route('/add', methods=["POST"])
def add():
   payload = request.form
   print('#### payload #### : ', payload)

   username = payload['username']
   email = payload['email']
   print('#### Data #### : ', username, ' / ', email)

   user = User(username=username, email=email)
   db.session.add(user)
   db.session.commit()

   return redirect(url_for('userList'))
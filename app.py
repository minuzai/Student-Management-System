import os
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
@app.route('/newUser')
def newUser():
   return render_template('newUser.html.j2', title='추가')

# 유저 정보 Page
@app.route('/userDetail/<id>/')
def userDetail(id):
   assignments = Assignment.query.filter_by(user_id = id)
   user = User.query.filter_by(id=id).one()
   print('#### assignments #### : ', assignments, id)
   print('#### user #### : ', user, id)
   return render_template('userDetail.html.j2', assignments=assignments, user=user)

# 유저 추가 End Point
@app.route('/addUser', methods=["POST"])
def addUser():
   payload = request.form
   print('#### payload #### : ', payload)

   username = payload['username']
   email = payload['email']
   print('#### Data #### : ', username, ' / ', email)

   user = User(username=username, email=email)
   db.session.add(user)
   db.session.commit()

   return redirect(url_for('userList'))

# 과제 및 점수 추가 End Point
@app.route('/addAssignment/<id>', methods=["POST"])
def addAssignment(id):
   payload = request.form
   print('#### payload #### : ', payload)

   assignment_title = payload['title']
   score = payload['score']
   user_id = id
   print('#### Data #### : ', assignment_title, ' / ', score)

   assignment = Assignment(assignment_title=assignment_title, score=score, user_id=user_id)
   db.session.add(assignment)
   db.session.commit()

   return redirect(url_for('userList'))

if __name__ == "__main__":
   port = int(os.environ.get("PORT", "5000"))
   app.run(host="0.0.0.0", port=port)
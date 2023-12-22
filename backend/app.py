from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request, abort
from sqlalchemy.orm import validates


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
@app.route('/')
def home():
    return jsonify(message='Welcome to the Task Manager API')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    
@validates('task_id')
def validate_task_id(self, key, value):
        if not isinstance(value, int):
            raise ValueError('Task ID must be an integer')
        return value    

# Defined models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    
@validates('username')
def validate_username(self, key, value):
        if not value.isalpha():
            raise ValueError('Username must contain only letters')
        return value
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='task', lazy=True)

class TaskTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', secondary='task_tags', backref='tags')

# Created the many-to-many association table
task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('task_tag.id'), primary_key=True)
)
@app.route('/api/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})

    elif request.method == 'GET':
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username} for user in users])

# Created and Read for Comment
@app.route('/api/comments', methods=['POST', 'GET'])
def comments():
    if request.method == 'POST':
        data = request.get_json()
        new_comment = Comment(text=data['text'], task_id=data['task_id'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comment created successfully'})

    elif request.method == 'GET':
        comments = Comment.query.all()
        return jsonify([{'id': comment.id, 'text': comment.text, 'task_id': comment.task_id} for comment in comments])

# Create and Read for TaskTag
@app.route('/api/tasktags', methods=['POST', 'GET'])
def task_tags():
    if request.method == 'POST':
        data = request.get_json()
        new_tasktag = TaskTag(tag=data['tag'])
        db.session.add(new_tasktag)
        db.session.commit()
        return jsonify({'message': 'TaskTag created successfully'})

    elif request.method == 'GET':
        tasktags = TaskTag.query.all()
        return jsonify([{'id': tasktag.id, 'tag': tasktag.tag} for tasktag in tasktags])
    
@app.route('/api/tasks', methods=['OPTIONS', 'POST'])
def handle_preflight():
    return '', 200

    return jsonify({'message': 'Task created successfully'})
# API routes
# Full CRUD for Task
@app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'GET':
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description})

    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

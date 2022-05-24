# from crypt import methods
# from crypt import methods
# from email.policy import default
import sys
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:321@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False )
    completed = db.Column(db.Boolean,nullable=False, default=False)

    def __repr__(self) :
        return f'Todo {self.id} {self.description}'
db.create_all()

@app.route('/todos/<todoId>delete', methods=['POST'])
def delete_todos(todoId):
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todoId>update', methods=['POST'])
def update_todos(todoId):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todoId)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body ['description'] = todo.description
    except:
        error =True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
        

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())
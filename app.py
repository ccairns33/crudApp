from cProfile import run
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app) #initalizing database

# DB MODEL
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}> {self.content}"

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['input-content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task."

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        # new conent is set from the data in the input field
        task_to_update.content = request.form["input-content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating your task"
    else:
        return render_template("update.html", task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)
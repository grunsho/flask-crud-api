from flask import Flask, redirect, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request

# App setup
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    # due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Task {self.id}"


with app.app_context():
    db.create_all()


# Routes

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    # Add a task
    if request.method == "POST":
        current_task = request.form["description"]
        new_task = MyTask(description=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created_at).all()
        return render_template("index.html", tasks=tasks)

# Delete an Item


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"

# Edit an item


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task_to_edit = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task_to_edit.description = request.form["description"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        return render_template("edit.html", task=task_to_edit)


# Runner and Debugger
if __name__ == "__main__":
    app.run(debug=True)

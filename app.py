from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id =        db.Column(db.Integer,primary_key=True)
    title =     db.Column(db.String(200),nullable=False)
    amount =    db.Column(db.Integer)
    category = db.Column(db.String(200),nullable=False)
    date     = db.Column(db.DateTime,default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    all_expenses = Expense.query.all()
    total_spent = 0

    for expense in all_expenses:
        total_spent = total_spent + expense.amount

    return render_template(
        "index.html",
        all_expenses=all_expenses,
        total=total_spent
    )


@app.route("/add", methods=["POST"])              
def add_expense():
    title = request.form.get("title")
    amount= request.form.get("amount")
    category=request.form.get("category")

    new_expense = Expense (
        title = title,
        amount = amount,
        category = category

    )

    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:id>")              
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:id>", methods=["GET","POST"])              
def update_expense(id):
    expense = Expense.query.filter_by(id=id).first()

    if request.method == "POST":
        expense.title = request.form.get("title")
        expense.amount = request.form.get("amount")
        expense.category =request.form.get("category")
    
        db.session.commit()
        return redirect("/")

    return render_template("update.html",expense=expense)


if __name__=="__main__":
    app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class mydata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ID is: {int(self.id)}"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data = request.form["todo"]
        if not isinstance(data, (str)):
            return redirect("/")
        else:
            new_data = mydata(post=data)
            db.session.add(new_data)
            db.session.commit()

            return redirect("/")
    
    else:
        display_data = mydata.query.order_by(mydata.date_posted).all()
        
        
        return render_template("index.html", display_data=display_data)


@app.route("/delete/<int:id>")
def delete(id):
    delete_data = mydata.query.get_or_404(id)
    db.session.delete(delete_data)
    db.session.commit()

    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
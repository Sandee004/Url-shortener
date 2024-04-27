from datetime import datetime
import random
import string
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)

class Shortener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_link = db.Column(db.String(255))
    short_link = db.Column(db.String(30), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
        db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        long_link = request.form.get("url")
        short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

        new_link = Shortener(long_link=long_link, short_link=short_link)
        db.session.add(new_link)
        db.session.commit()

        generated_short_link = new_link.short_link

        success_message = f"Long link successfully shortened! Your short link is: http://localhost:80/{generated_short_link}"

        # Pass shortened link and message to the template
        context = {
            "success_message": success_message,
        }
        return render_template("index.html", **context)  # Unpack the dictionary

    return render_template("index.html")
    

@app.route('/database')
def database():
    links = Shortener.query.all()
    return render_template("database.html", links=links)


@app.route('/<short_code>')
def redirect_to_long_link(short_code):
    link = Shortener.query.filter_by(short_link=short_code).first()
    if link:
        return redirect(link.long_link)
    else:
        return "Link not found."



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=False)

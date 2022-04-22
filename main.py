from flask import Flask, url_for, redirect, request, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'y3ferteryukeymmrester'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/profile/<id>")
def profile(id, name):
    return render_template("profile.html", name=name)

if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
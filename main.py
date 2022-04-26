from flask import Flask, url_for, redirect, request, render_template
from forms import *
from data.users import *
from data import db_session
from flask import session
import datetime

from VARS import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'y3ferteryukeymmrester'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route("/")
def index():
    print(session["log"])
    log = session.get('log', False)
    if not log:
        session["log"] = log

    return render_template("index.html", USER_IN=session["log"])

@app.route("/quit")
def quit():
    log = session.get('log', False)
    if not log:
        session["log"] = log
    session.pop("email")
    session["log"] = False
    return redirect("/")
@app.route("/signin", methods=['GET','POST'])
def signin():
    log = session.get('log', False)
    if not log:
        session["log"] = log
    if session["log"]:
        return redirect("/")

    form = LoginForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email==form.email.data).first()
        if user.check_password(form.password.data):
            em = session.get('email', user.email)
            session["email"] = user.email
            session["log"] = True
            return redirect('/')
    return render_template("signin.html", form=form, USER_IN=session["log"] )

@app.route("/signup", methods=['GET','POST'])
def signup():
    log = session.get('log', False)
    if not log:
        session["log"] = False
    if session["log"]:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_2.data:
            return render_template("signup.html",
                                   form=form,
                                   message="Пароли не совпадают", USER_IN=session["log"])
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("signup.html",
                                   form=form,
                                   message="Такой пользователь уже есть", USER_IN=session["log"])
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/signin')
    return render_template("signup.html", form=form, USER_IN=session["log"])


@app.route("/profile", methods=['GET','POST'])
def profile():
    log = session.get('log', False)
    if not log:
        session["log"] = log
    if session["log"]:
        form = ProfileForm()
        toker = session.get('token', None)
        sums = session.get('sum', None)
        codee = session.get('codes', None)
        if sums is None:
            session["sum"] = None
        if toker is None:
            session["token"] = None
        if codee is None:
            session["codes"] = None
        if form.validate_on_submit():
            session["token"] = form.tokens.data
            session["sum"] = form.sumer.data
            session["codes"] = f"{form.codeword1.data},{form.codeword2.data},{form.codeword3.data}"
        if codee is None and toker is None and sums is None:
            return render_template("profile.html", name=session["email"], form=form,
                                   sum=0, none=None,USER_IN=session["log"])
        return render_template("profile.html", name=session["email"], form=form, token=session["token"],
                               sum=session["sum"], code=session["codes"], none=None,USER_IN=session["log"])

    return redirect("/signin")

if __name__ == "__main__":
    db_session.global_init("db/base.db")
    app.run(port=8080, host='127.0.0.1')
1
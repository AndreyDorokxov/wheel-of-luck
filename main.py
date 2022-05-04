from flask import Flask, url_for, redirect, request, render_template
from forms import *
from wheel_logic import *
from data.users import *
from data import db_session
from flask import session
import datetime
import VARS
from donationalerts import Alert
app = Flask(__name__)
app.config['SECRET_KEY'] = 'y3ferteryukeymmrester'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route("/")
def index():
    global alert
    loged()
    print(VARS.event_list)
    print(VARS.event_codes)
    print(VARS.n)

    if session["eventer"] is None:
        return render_template("index.html", USER_IN=session["log"],  trues=session["eventer"], none=None)
    else:
        if VARS.n == 0:
            alert = Alert(session["token"])

            @alert.event()
            def handler(event):
                if not (VARS.event_codes is None):
                    a1 = event.message
                    a2 = event.amount
                    n = 0

                    for i in VARS.event_codes:
                        if str(a1) == str(i):
                            VARS.event_list[n] += float(a2)
                        n += 1

            VARS.n = 1

        session["eventer"] = VARS.event_list
        wheel = Wheel(session["eventer"])
        chance = []
        for i in wheel.calculate():
            chance.append(int(i * 100))

        return render_template("index.html", USER_IN=session["log"], code=session["codes"], events=wheel.calculate(),
                               trues=session["eventer"], none=None, chance=chance)


@app.route("/quit")
def quiter():
    loged()

    session.pop("email")
    session["log"] = False
    session.pop("token")
    session.pop("eventer")
    session.pop("codes")
    return redirect("/")


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    loged()

    if session["log"]:
        return redirect("/")

    form = LoginForm()
    db_sess = db_session.create_session()

    if form.validate_on_submit():
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user.email == form.email.data:
            if user.check_password(form.password.data):
                em = session.get('email', user.email)
                session["email"] = user.email
                session["log"] = True
                return redirect('/')
            else:
                return redirect('/signin')

    return render_template("signin.html", form=form, USER_IN=session["log"])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    loged()

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
            email=form.email.data,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect('/signin')

    return render_template("signup.html", form=form, USER_IN=session["log"])


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    loged()
    if session["log"]:
        form = ProfileForm()

        if form.validate_on_submit():
            session["token"] = form.tokens.data
            session["codes"] = [form.codeword1.data,
                                form.codeword2.data, form.codeword3.data]
            session["eventer"] = [1.0, 1.0, 1.0]
            VARS.n = 0
        if session["codes"] is None and session["token"] is None and session["sum"] is None:
            return render_template("profile.html", name=session["email"], form=form,
                                   sum=0, none=None, USER_IN=session["log"])

        return render_template("profile.html", name=session["email"], form=form, token=session["token"],
                               sum=session["sum"], code=session["codes"], none=None, USER_IN=session["log"])

    return redirect("/signin")

# проверка session используется везде.


def loged():

    log = session.get('log', False)
    if not log:
        session["log"] = log

    toker = session.get('token', None)
    codee = session.get('codes', None)
    eventer = session.get('eventer', None)

    if toker is None:
        session["token"] = None

    if codee is None:
        session["codes"] = None

    if eventer is None:
        session["eventer"] = None

    VARS.event_codes = session["codes"]
    VARS.token = session["token"]

    if VARS.n == 0 and not session["eventer"] is None:
        VARS.event_list = session["eventer"]
        VARS.event_codes = session["codes"]


if __name__ == "__main__":
    db_session.global_init("db/base.db")
    app.run(port=8080, host='127.0.0.1')

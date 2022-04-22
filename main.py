from flask import Flask, url_for, redirect, request, render_template
from donationalerts.asyncio_api import DonationAlertsAPI, Centrifugo
from donationalerts.constants import Scopes, Channels

app = Flask(__name__)
app.config['SECRET_KEY'] = 'y3ferteryukeymmrester'
api = DonationAlertsAPI("9429", "DqARHFdlNjLIlwa5YSYlXhfWySMzqhRWVZwP9ipX", "http://127.0.0.1:5000/login",
                        Scopes.ALL_SCOPES)


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


@app.route("/", methods=["GET"])
def index():
    return redirect(api.login())


@app.route("/login", methods=["GET"])
async def login():
    code = request.args.get("code")
    access_token = await api.get_access_token(code)
    user = await api.user(access_token)

    fugo = Centrifugo(user.socket_connection_token, access_token, user.id)
    event = await fugo.subscribe(Channels.NEW_DONATION_ALERTS)
    return event.objects


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')

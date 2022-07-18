from flask import Flask, render_template, request, abort, send_file, session
from flask.sessions import SecureCookieSessionInterface
from pathlib import Path
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "p5VAmUfaP71Zpy1g"

session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)


ROOT = Path(__file__).parent
FILES = json.loads((ROOT / "files.json").read_text())


@app.route("/")
def get_leaks():
    if "is_admin" not in session:
        session["is_admin"] = 0

    return render_template("leaks.html", files=FILES)


@app.route("/flag")
def get_flag():
    if session.get("is_admin") == 1:
        return "Welcome to our family. " + os.environ["FLAG"]
    else:
        return "You're not an admin :("


@app.route("/download")
def download_file():
    filename = request.args.get("filename")
    if not filename:
        abort(400)
    
    if ".." in filename:
        abort(400)

    try:
        if not (ROOT / filename).is_file():
            abort(404)
    except ValueError:
        abort(400)

    return send_file(filename, attachment_filename=os.path.basename(filename))

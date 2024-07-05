import random
import uuid
from flask import Flask, Response, make_response, url_for
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = random.randint(2 ^ 127, 2 ^ 128).to_bytes(16, 'big')
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)

flag = open("flag.txt").read().encode()
ngrams = [flag[start:start + 4] for start in range(len(flag) - 3)]


@app.after_request
def waf(response: Response) -> Response:
    print(f"Response: {response.data}")
    if any([ngram in response.data for ngram in ngrams]):
        return Response(status=401)
    else:
        return response


@app.route("/flag")
@jwt_required()
def get_flag() -> Response:
    current_user = get_jwt_identity()
    if current_user == "admin":
        return Response(flag)
    else:
        return Response(status=403)


@app.route("/login")
def login() -> Response:
    access_token = create_access_token(identity=uuid.uuid4())
    res = make_response()
    res.status = 302
    res.set_cookie("access_token_cookie", value=access_token)
    res.headers['location'] = url_for('hello')
    return res


@app.route("/hello")
@jwt_required()
def hello() -> str:
    current_user = get_jwt_identity()
    return f"<h1>Hello {current_user}</h1>"


@app.route("/")
def get_root() -> str:
    return '<a href="/login">Login!</a>'


if __name__ == "__main__":
    app.run(host="0.0.0.0")

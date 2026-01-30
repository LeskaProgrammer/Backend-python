from flask import Flask, jsonify, request
from dotenv import dotenv_values
from typing import Union

from controllers import operation

app = Flask(__name__)


def get_port() -> int:
    config = dotenv_values(".env")
    if "PORT" in config:
        return int(config["PORT"])
    return 5000


@app.route("/")
def server_info() -> str:
    return "My server"


@app.route("/author")
def author() -> str:
    author_info = {
        "name": "Lesha",
        "course": 3,
        "age": 21,
    }
    return jsonify(author_info)


@app.route("/sum")
def runner() -> str:
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    return jsonify({'sum': operation(a, b)})


if __name__ == "__main__":
    app.run(debug=True, port=get_port())
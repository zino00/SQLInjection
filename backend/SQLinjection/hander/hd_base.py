import functools

import flask
from flask import Flask

from flask import request, make_response
app = Flask(__name__)

def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                if arg not in request.json:
                    return flask.abort(400)
            return func(*args, **kw)
        return wrapper
    return decorator

@app.errorhandler(400)
def not_found(error):
     return make_response(flask.jsonify({'error': '参数不正确'}), 400)
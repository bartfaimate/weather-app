import flask
from routers.router import api


import logging

log = logging.getLogger(__file__)

def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(api)

    log.info("Generating jwt key")
    from utils.jwt import Jwt

    key = Jwt.create_key()
    try:
        Jwt.save_key_to_file(key)
    except OSError as e:
        log.warning(e)

    return app


def page_not_found(e):
    return flask.jsonify({"message": "Page not found"}), 404

def internal_server_error(e):
    return flask.jsonify({"message": f"Internal server error {e}"}), 500

def bad_request(e):
    return flask.jsonify({"message": f"Bad request {e} "}), 400

def unauthorized(e):
    return flask.jsonify({"message": "Unauthorized"}), 401


if __name__ == '__main__':
    app = create_app()

    app.register_error_handler(400 , bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter

from config import Dev

app = Flask(__name__)
app.secret_key = Dev.SECRET_KEY
app.config.from_object(Dev)
# db_session = Configuration.DB_SESSION
db = SQLAlchemy(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('support_scripts.log', 'a', 1 * 1024 ** 3, 3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addFilter(file_handler)
    app.logger.info('support_scripts started')


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

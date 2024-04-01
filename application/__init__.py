import os
from flask import Flask
from .blueprints import auth_bp,user_profile_bp,views
from flask_login import LoginManager
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(views)
    from .database import init_app
    init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'application.sqlite'))
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    return app

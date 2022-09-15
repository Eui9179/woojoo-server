import os
import sys

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.pool import QueuePool
from woojoo.utils.cdn import CDN

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
base_dir = os.getcwd()
sys.path.append(base_dir)
app.config.from_pyfile(f"{base_dir}/woojoo/default.cfg")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "poolclass": QueuePool,
    "pool_size": 10,
    'pool_pre_ping': True
}

CORS(app, supports_credentials=True)
jwt = JWTManager(app)
cdn = CDN()

from woojoo.models import *
db.init_app(app)
migrate.init_app(app, db)

from woojoo.controllers.auth import auth_bp
from woojoo.controllers.user import user_bp
from woojoo.controllers.game import game_bp
from woojoo.controllers.admin import admin_bp
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(game_bp)
app.register_blueprint(admin_bp)
from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

from woojoo.controllers.user.profile import *
from woojoo.controllers.user.friends import *
from woojoo.controllers.user.groups import *
from flask import Blueprint

game_bp = Blueprint("game", __name__, url_prefix="/api/games")

from woojoo.controllers.game.my_game import *
from woojoo.controllers.game.todays_game import *
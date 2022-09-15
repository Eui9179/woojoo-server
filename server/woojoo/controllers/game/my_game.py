from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo import db
from woojoo.models.games import UserGames
from woojoo.models.user import User
from woojoo.controllers.game import game_bp
from woojoo.utils.common import (
    response_json_with_code,
)


@game_bp.route('/me', methods=["POST"])
@jwt_required()
def update_my_game_list():
    game_list = request.get_json();
    user_id = get_jwt_identity()
    
    user_row = User.get_user_by_id(user_id)
    game_rows = UserGames.get_games_by_user_id(user_id)
    my_games = [game.game for game in game_rows]
    
    if user_row:
        for game in my_games: # 삭제할 게임
            if not game in game_list:
                UserGames.query.filter((UserGames.user_id==user_id)&(UserGames.game==game)).delete()
            
        for game in game_list: # 추가할 게임
            if not game in my_games:
                db.session.add(UserGames(user_id=user_id, game=game))
            
        # objects = []
        
        # for game in game_list:
        #     objects.append(UserGames(user_id=user_id, game=game))
        
        # db.session.add_all(objects)
        db.session.commit()
        
        game_rows = UserGames.get_games_by_user_id(user_id)
        res = [{'game':game_row.game, 'nickname': game_row.nickname} for game_row in game_rows]
        
        return response_json_with_code(my_games = res)
    
    return response_json_with_code(res_code=403)

@game_bp.route('/me', methods=["GET"])
@jwt_required()
def get_my_game_list():
    user_id = get_jwt_identity()
    my_games_row = UserGames.get_games_by_user_id(user_id)
    my_games = []
    
    for my_game in my_games_row:
        my_games.append({
            'game':my_game.game,
            'nickname':my_game.nickname
        })
            
    return response_json_with_code(my_games = my_games)


@game_bp.route('/nickname', methods=["POST"])
@jwt_required()
def update_game_nickname():
    user_id = get_jwt_identity()
    req = request.get_json();
    game = req['game']
    nickname = req['nickname']
    
    game_row = UserGames.get_game_one_by_user_id(user_id, game)
    game_row.nickname = nickname
    db.session.commit()
            
    return response_json_with_code()
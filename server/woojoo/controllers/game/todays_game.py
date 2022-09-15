from threading import Thread
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo import db
from ...models.games import UserGames
from woojoo.models.todays_games import TodaysGames
from woojoo.models.user import User
from woojoo.controllers.game import game_bp
from woojoo.utils.common import (
    response_json_with_code,
)
from datetime import datetime, timedelta
from pytz import timezone
from operator import itemgetter
import requests, json

header = {
        'Content-Type': 'application/json; chearset=utf-8',
        'Authorization':'key=AAAA5YBAC-M:APA91bEJI3-JRSLzrKYoqbj9DJ_f7mbAdhLa-n-2SKEaqtrrcXbCezbQgBG5IBrZ7JQKfUjD8px4GSPaWmWkgaJfV8eC7eGDAFMdndzn-NW8Z7cdvGHZBin7G4jLklGNwWOFaGrdXpUc'
    }

@game_bp.route('/todays-test', methods=["GET"])
@jwt_required()
def test_todays_game():
    KST = timezone('Asia/Seoul')
    create_time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    user_id = get_jwt_identity()
    
    user_row = User.get_user_by_id(user_id)
    game_row = UserGames.get_games_by_user_id(user_id);
    
    db.session.add(TodaysGames(
        user_id=user_id, 
        game=game_row[0].game, 
        introduction='ㄱㄱ',
        create_time=create_time
    ))
    db.session.commit()
    
    fcm_tokens =  db.engine.execute(
        f'SELECT fcm_token FROM user WHERE id IN (SELECT friend_id FROM friends WHERE user_id={user_id});'
    )
    
    thread = Thread(
        target=send_notification, 
        args=(fcm_tokens, user_row.name, game_row[0].game, 'ㄱㄱ')
    )
    thread.daemon = True
    thread.start()

    
    return response_json_with_code()

@game_bp.route('/todays', methods=["POST"])
@jwt_required()
def insert_todays_games():
    req = request.get_json();
    user_id = get_jwt_identity()
    
    TodaysGames.create_todays_game(
        user_id=user_id,
        game=req['game'],
        introduction=req['introduction']
    )
    
    user_row = User.get_user_by_id(user_id)
    
    if not user_row:
        return response_json_with_code(res_code=404)
    
    fcm_tokens =  db.engine.execute(
        f'SELECT fcm_token FROM user WHERE id IN (SELECT friend_id FROM friends WHERE user_id={user_id});'
    )
    
    thread = Thread(
        target=send_notification, 
        args=(fcm_tokens, user_row.name, req['game'], req['introduction'])
    )
    thread.daemon = True
    thread.start()
    
    return response_json_with_code()

def send_notification(fcm_tokens, name, game, introduction):
    for fcm in fcm_tokens:
        print(fcm.fcm_token)
        dict = {
            'to' : fcm.fcm_token,
            'priority' : 'high', 
            'notification' : {
                'title' : name +'님의 오늘의 게임',
                'body' : changeKorGameName(game) + ' - ' + introduction
            }
        }
        res = requests.post('https://fcm.googleapis.com/fcm/send',headers=header, data=json.dumps(dict))
        print(res.status_code)
        
        
@game_bp.route('/todays', methods=["GET"])
@jwt_required()
def get_todays_games():
    user_id = get_jwt_identity()
    KST = timezone('Asia/Seoul')
    
    today = datetime.now().astimezone(KST).strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).astimezone(KST).strftime('%Y-%m-%d')
    
    todays_games = db.engine.execute(
        f'SELECT * FROM todays_games \
            WHERE create_time BETWEEN "{today}" AND "{tomorrow}" \
            AND user_id IN (SELECT friend_id FROM friends WHERE user_id={user_id});'
    )
    
    my_todays_games = db.engine.execute(
        f'SELECT * FROM todays_games \
            WHERE create_time BETWEEN "{today}" AND "{tomorrow}" \
            AND user_id={user_id};'
    )
    
    res = []

    for todays_game in todays_games:
        user_row = User.get_user_by_id(todays_game.user_id)
        
        if not user_row:
            continue
        
        game_row = UserGames.get_game_one_by_user_id(todays_game.user_id, todays_game.game)
        
        if not game_row:
            continue
        
        res.append({
            'todays_game_id':todays_game.id,
            "id": user_row.id,
            "name": user_row.name,
            "profile_image_name":user_row.profile_image_name,
            'game': todays_game.game,
            'game_nickname': game_row.nickname,
            'introduction':todays_game.introduction,
            'create_time':todays_game.create_time,
            'isme':False
        })
    
    for my_todays_game in my_todays_games:
        user_row = User.get_user_by_id(my_todays_game.user_id)
        
        if not user_row:
            continue
        
        game_row = UserGames.get_game_one_by_user_id(user_id, my_todays_game.game)
        
        if not game_row:
            continue
      
        res.append({
            'todays_game_id':my_todays_game.id,
            "id": user_row.id,
            "name": user_row.name,
            "profile_image_name":user_row.profile_image_name,
            'game': my_todays_game.game,
            'game_nickname': game_row.nickname,
            'introduction':my_todays_game.introduction,
            'create_time':my_todays_game.create_time,
            'isme':True
        })
    
    newres = sorted(res, key=itemgetter('create_time'), reverse=True)
    
    return response_json_with_code(result = newres)

@game_bp.route('todays/<int:today_game_id>', methods=['DELETE'])
@jwt_required()
def delete_todays_game(today_game_id):
    user_id = get_jwt_identity()
    TodaysGames.query.filter(
        (TodaysGames.id==today_game_id) & 
        (TodaysGames.user_id==user_id)
    ).delete()
    
    db.session.commit()
    
    return response_json_with_code()

def changeKorGameName(game_name) :
    game = {
        'leagueoflegends':'리그 오브 레전드',
        'overwatch':'오버워치',
        "valorant": "발로란트",
        "tft": "전략적 팀 전투",
        "battleground": "배틀그라운드",
        "lostark": "로스트아크",
        "minecraft": "마인크래프트",
        "fifaonline4": "피파 온라인4",
        "starcraft": "스타크래프트",
        "overwatch": "오버워치",
        "starcraft2": "스타크래프트2",
        "counterstrike": "카운터스트라이크",
        "apexlegends": "에픽 레전드",
        "fortnite": "포트나이트",
        "gta5": "gta 5",
        "dota2": "도타 2",
        "fallguys": "폴가이즈",
        "callofduty": "콜오브듀티",
        "worldofwarcraft": "월드오브워크래프트",
        "hearthstone": "하스스톤",
        "maplestory": "메이플스토리",
        "suddenattack": "서든어택",
        "dungeonandfighter": "던전앤파이터",
        "diablo2": "디아블로2",
        "roblox": "로블록스",   
    }
    return game[game_name]
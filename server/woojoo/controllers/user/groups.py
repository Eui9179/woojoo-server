from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo.controllers.user import user_bp
from woojoo.models.friends import Block, Friends
from woojoo.models.games import UserGames
from woojoo.models.groups import UserGroups
from woojoo.models.user import User
from woojoo.utils.common import response_json_with_code
from woojoo import db
from operator import itemgetter
import random

groups = [
    "상일초등학교",
    "상일중학교",
    "상원고등학교",
    "상원초등학교",
    "석천초등학교",
    "석천중학교",
    "부천정보산업고등학교",
    "상동초등학교",
];

@user_bp.route('friend/test3', methods=["GET"])
def test3_friend():
    tmp = ['+8201076246575', '+8201024873147', '+8201022272431', '+8201099775468', '+8201055406101', '+8201083952133', '+8201056167375', '+8201077644184', '+8201097959788', '+8201042244824', '+8201046964583', '+8201077028921', '+8201048541672', '+8201028891724', '+8201076694648', '+8201023859698', '+8201027405475', '+8201026739484', '+8201026312413', '+8201058259811', '+8201029222661', '+8201031393098', '+8201071295363', '+8201024872584', '+8201050246179']
    for t in tmp:
        user_row = User.get_user_by_phone_number(t)
        if user_row:
            db.session.add(UserGroups(
                user_id = user_row.id,
                name = "상일초등학교",
                detail1 = "3"
            ))
    
    db.session.commit()
    return response_json_with_code()

@user_bp.route('groups/me', methods=["GET"])
@jwt_required()
def get_my_groups():
    user_id = get_jwt_identity();
    group_rows = UserGroups.get_groups_by_user_id(user_id)
    my_groups = []
    for group in group_rows:
        my_groups.append({
            "name":group.name,
            "detail1":group.detail1
        })
    
    my_groups.sort()
        
    return response_json_with_code(my_groups = my_groups)


@user_bp.route('groups/<name>', methods=['GET'])
@jwt_required()
def get_people_by_group(name):
    user_id = get_jwt_identity()
    my_game_rows = UserGames.get_games_by_user_id(user_id)
    my_games = [my_game.game for my_game in my_game_rows]
    
    my_friend_rows = Friends.get_friends_by_user_id(user_id)
    my_friends = [my_friend.friend_id for my_friend in my_friend_rows]
    
    my_block_rows = Block.get_block_by_user_id(user_id)
    my_block_user_ids = [my_block.friend_id for my_block in my_block_rows]
    
    group_rows = db.engine.execute(
        f'SELECT * FROM user WHERE id IN \
            (SELECT user_id FROM user_groups WHERE name="{name}");'
    )
    
    # 내 친구 목록의 친구 id와 User테이블, Game테이블 조인
    people = []
    friends = []
    
    for row in group_rows:
        if (row.id not in my_block_user_ids):
            friend_game_rows = UserGames.get_games_by_user_id(row.id)
            friend_games = [friend.game for friend in friend_game_rows]
            intersection = list(set(my_games).intersection(friend_games))
            if row.id != user_id:
                if not row.id in my_friends:
                    people.append({
                        "id": row.id,
                        "name": row.name,
                        "profile_image_name": row.profile_image_name,
                        "games": intersection,
                    })
                else:
                    
                    friends.append({
                        "id": row.id,
                        "name": row.name,
                        "profile_image_name": row.profile_image_name,
                        "games": intersection,
                    })
                
    sorted_people = sorted(people, key=itemgetter('name'))
    sorted_friends = sorted(friends, key=itemgetter('name'))
        
    return response_json_with_code(people = sorted_people, friends = sorted_friends)


@user_bp.route('groups/<name>/<detail1>', methods=['GET'])
@jwt_required()
def get_people_by_group_detail1(name, detail1):
    user_id = get_jwt_identity()
    my_game_rows = UserGames.get_games_by_user_id(user_id)
    my_games = [my_game.game for my_game in my_game_rows]
    
    my_friend_rows = Friends.get_friends_by_user_id(user_id)
    my_friends = [my_friend.friend_id for my_friend in my_friend_rows]
    
    my_block_rows = Block.get_block_by_user_id(user_id)
    my_block_user_ids = [my_block.friend_id for my_block in my_block_rows]
    
    group_rows = db.engine.execute(
        f'SELECT * FROM user WHERE id IN \
            (SELECT user_id FROM user_groups WHERE name="{name}" AND detail1="{detail1}");'
    )
    # 내 친구 목록의 친구 id와 User테이블, Game테이블 조인
    people = []
    friends = []
    
    for row in group_rows:
        if (row.id not in my_block_user_ids):
            friend_game_rows = UserGames.get_games_by_user_id(row.id)
            friend_games = [friend.game for friend in friend_game_rows]
            intersection = list(set(my_games).intersection(friend_games))
            if row.id != user_id:
                if not row.id in my_friends:
                    people.append({
                        "id": row.id,
                        "name": row.name,
                        "profile_image_name": row.profile_image_name,
                        "games": intersection,
                    })
                else:
                    friends.append({
                        "id": row.id,
                        "name": row.name,
                        "profile_image_name": row.profile_image_name,
                        "games": intersection,
                    })
                
    sorted_people = sorted(people, key=itemgetter('name'))
    sorted_friends = sorted(friends, key=itemgetter('name'))
        
    return response_json_with_code(people = sorted_people, friends = sorted_friends)
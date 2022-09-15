from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo.controllers.user import user_bp

from woojoo.models.friends import Friends
from woojoo.models.games import UserGames
from woojoo.models.groups import UserGroups
from woojoo.models.user import User
from woojoo.utils.common import response_json_with_code
from woojoo import db, cdn
from operator import itemgetter


@user_bp.route('profile/me', methods=["GET"])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity();
    user_row = User.get_user_by_id(user_id)
    if user_row:
        return response_json_with_code(my_profile = user_row.to_dict())
    else:
        return response_json_with_code(res_code=401)


@user_bp.route('profile/<int:user_id>', methods=["GET"])
@jwt_required()
def get_user_profile(user_id):
    my_id = get_jwt_identity()
    
    my_friend_rows = Friends.get_friends_by_user_id(my_id)
    my_friends = [my_friend_row.friend_id for my_friend_row in my_friend_rows]
    
    my_game_rows = UserGames.get_games_by_user_id(my_id)
    my_games = [my_game_row.game for my_game_row in my_game_rows]
        
    user_profile_row = User.get_user_by_id(user_id)
    
    user_group_rows = UserGroups.get_groups_by_user_id(user_id)
    user_groups = [
        {
            "name":user_group_row.name,
            "detail1":user_group_row.detail1
        } for user_group_row in user_group_rows]
    
    user_game_rows = UserGames.get_games_by_user_id(user_id)
    user_games = [
        {'game':user_game_row.game, 
         'nickname':user_game_row.nickname} for user_game_row in user_game_rows
    ]
    
    is_friend = False;
    if user_profile_row.id in my_friends:
        is_friend = True
    
    user_friend_rows = db.engine.execute(f"SELECT * FROM user WHERE id IN (SELECT friend_id FROM friends WHERE user_id={user_id});")
    
    user_friends = []
    already_friends = []
    
    for user_friend_row in user_friend_rows:
        if user_friend_row.id != my_id:
            friend_game_rows = UserGames.get_games_by_user_id(user_friend_row.id)
            friend_games = [friend.game for friend in friend_game_rows]
            intersection = list(set(my_games).intersection(friend_games))
            
            if (user_friend_row.id in my_friends):
                # 나랑 이미 친구
                already_friends.append({
                    "id": user_friend_row.id,
                    "name": user_friend_row.name,
                    "profile_image_name": user_friend_row.profile_image_name,
                    "games": intersection,
                })
            else: 
                # 나는 모르는 사람
                user_friends.append({
                    "id": user_friend_row.id,
                    "name": user_friend_row.name,
                    "profile_image_name": user_friend_row.profile_image_name,
                    "games": intersection,
                })

    sorted_already_friends = sorted(already_friends, key=itemgetter('name'))                
    sorted_user_friends = sorted(user_friends, key=itemgetter('name'))
    
    user_profile = {
        "user_id":user_profile_row.id,
        "name": user_profile_row.name,
        "profile_image_name":user_profile_row.profile_image_name,
    }
    
    return response_json_with_code(
        user_profile=user_profile, 
        is_friend = is_friend,
        user_groups=user_groups,
        user_games=user_games,
        already_friends = sorted_already_friends,
        user_friends=sorted_user_friends,
    )
    

@user_bp.route('/setting', methods=["POST"])
@jwt_required()
def setting_profile():
    user_id = get_jwt_identity()
    
    
    name = request.form.get("name")
    file = request.files.get("file")
    is_file = request.form.get("is_file")
    
    # 그룹이 하나일때만
    group_name = request.form.get('group_name')
    group_detail1 = request.form.get('group_detail1')
    is_group = request.form.get('is_group')
        
    user_row = User.get_user_by_id(user_id)
    if not user_row:
        return response_json_with_code(res_code=401)
    
    res_image_name = user_row.profile_image_name
    
    if is_file == 'true':
        if file:
            if user_row.profile_image_name != "default":
                cdn.delete_file(user_row.profile_image_name)
                
                # try:
                #     full_path = os.path.join(PROFILE_IMAGE_FILE_PATH, user_row.profile_image_name)
                #     os.remove(full_path)
                # except:
                #     pass
            
            filename = cdn.send_stream_image_file(file)
            # root, ext = os.path.splitext(file.filename)
            # now_time = int(time.time())
            # filename = f"profile_{now_time}{ext}"
            # full_path = os.path.join(PROFILE_IMAGE_FILE_PATH, filename)
            # file.save(full_path)
            
            
            user_row.profile_image_name = filename
            res_image_name = filename
        else:
            if user_row.profile_image_name != "default":
                cdn.delete_file(user_row.profile_image_name)
                # try:
                #     full_path = os.path.join(PROFILE_IMAGE_FILE_PATH, user_row.profile_image_name)
                #     os.remove(full_path)
                # except:
                #     pass
                
            user_row.profile_image_name = "default"
            res_image_name = "default"
        
    # 유저 이름
    if name:
        user_row.name = name
        
    if is_group == 'true':
        group_row = UserGroups.get_group_one_by_user_id(user_id)
        # # 그룹 이름
        # UserGroups.query.filter(UserGroups.user_id==user_id).delete() # 그룹 한개 가정
        # db.session.commit()
        
        # for group in groups:
        group_row.name = group_name
        group_row.detail1 = group_detail1
            # db.session.add(UserGroups(
            #     user_id = user_id,
            #     name = group['name'],
            #     detail1 = group['detail1']
            # ))
        
    db.session.commit()
    
    return response_json_with_code(res_image_name=res_image_name)
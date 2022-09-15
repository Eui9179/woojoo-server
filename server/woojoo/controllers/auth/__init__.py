from flask import Blueprint, request, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo import db, cdn
from woojoo.models.friends import Friends
from woojoo.models.games import UserGames
from woojoo.models.groups import UserGroups
from woojoo.models.user import User
from woojoo.utils.common import (
    response_json_with_code,
)
from woojoo.utils.jwt import JwtToken   

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

headers = {
    'Content-Type': 'application/json; chearset=utf-8',
    'Authorization':'key=AAAAgdsrYfY:APA91bFPnAbWgVS2NITYanribOeuBkTbB715mTGQzLNjo9W9waNmEjqMYOzzjbwbJilmla-6oA09qnddeIWAUpT_EUte9KJ5vHsBl4tM-jA-OLB29KjoS7vyeaFKL6c0MGfk7wRb7ksQ'
    }


@auth_bp.route('/signup', methods=["POST"])
def signup():
    name = request.form.get("name")
    phone_number = request.form.get("phone_number")
    file = request.files.get("file")
    fcm_token = request.form.get("fcm_token")
    
    groups = request.form.getlist("groups")
    detail1 = request.form.get("detail1")
    
    user_row = User.get_user_by_phone_number(phone_number)
    if user_row:
        return response_json_with_code(res_code=409, result="Conflict")
    
    if file:
        filename = cdn.send_stream_image_file(file)
    else:
        filename = "default"
        
    db.session.add(User(
        name = name,
        phone_number = phone_number,
        profile_image_name = filename,
        fcm_token = fcm_token,
    ))
    
    db.session.commit()
    
    user_id = User.get_user_by_phone_number(phone_number).id
    
    for group in groups:
        db.session.add(UserGroups(
            user_id = user_id,
            name = group,
            detail1 = detail1
        ))
        
    db.session.commit()
        
    tokens = JwtToken(user_id)
    resp = response_json_with_code(access_token=tokens.access_token)
    
    return resp

    
    
@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    phone_number = data['phone_number']
    fcm_token = data['fcm_token']
    user_row = User.get_user_by_phone_number(phone_number)
    
    if user_row is None:
        return response_json_with_code(
            401, 
            result="There is no ID on db."
        )
        
    if user_row.fcm_token != fcm_token:
        user_row.fcm_token = fcm_token
        db.session.commit()
    
    tokens = JwtToken(user_row.id)
    resp = response_json_with_code(access_token=tokens.access_token)
    
    return resp


@auth_bp.route('/withdrawal', methods=["DELETE"])
@jwt_required()
def withdrawal():
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    if user_row is None:
        return response_json_with_code(
            401, 
            result="There is no ID on db."
        )
    
    try:
        if user_row.profile_image_name != 'default':
            cdn.delete_file(user_row.profile_image_name)
    except:
        pass
    
    Friends.query.filter(Friends.user_id==user_id).delete()
    Friends.query.filter(Friends.friend_id==user_id).delete()
    UserGames.query.filter(UserGames.user_id==user_id).delete()
    UserGroups.query.filter(UserGroups.user_id==user_id).delete()
    User.query.filter(User.id==user_id).delete()
    
    db.session.commit()
    
    return response_json_with_code()

@auth_bp.route('/async-token', methods=['POST'])
@jwt_required()
def async_fcm_token():
    user_id = get_jwt_identity()
    fcm_token = request.get_json()['fcm_token']
    
    user_row = User.get_user_by_id(user_id)
    
    if user_row and user_row.fcm_token != fcm_token:
        user_row.fcm_token = fcm_token
        db.session.commit()
        
    return response_json_with_code()
    
        
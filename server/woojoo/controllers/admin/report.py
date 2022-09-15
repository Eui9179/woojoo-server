from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from woojoo import db
from woojoo.models.report import Report
from woojoo.controllers.admin import admin_bp
from woojoo.utils.common import (
    response_json_with_code,
)

@admin_bp.route('/report', methods=['POST'])
@jwt_required()
def create_report():
    report = request.get_json()
    
    user_id = get_jwt_identity()
    reported_user_id = report['reported_user_id']
    report_numbers = report['report_numbers']
    
    db.session.add(Report(
        user_id=user_id, 
        reported_user_id=reported_user_id, 
        report_numbers=report_numbers,
    ))
    
    db.session.commit()
    
    return response_json_with_code()
from woojoo import db

class UserGroups(db.Model):
    __tablename__ = "user_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    detail1 = db.Column(db.String(30), nullable=True)

    @staticmethod
    def get_groups_by_user_id(user_id):
        return UserGroups.query.filter(
            UserGroups.user_id==user_id
        ).all()
        
    @staticmethod
    def get_group_one_by_user_id(user_id):
        return UserGroups.query.filter(
            UserGroups.user_id==user_id
        ).one_or_none()
        
    @staticmethod
    def get_groups_by_name(name):
        return UserGroups.query.filter(
            UserGroups.name==name
        ).all()
    
    
    @staticmethod
    def insert_group(user_id, group, detail1):
        db.session.add(UserGroups(
            user_id=user_id,
            name=group,
            detail1=detail1,
        ))
        db.session.commit()
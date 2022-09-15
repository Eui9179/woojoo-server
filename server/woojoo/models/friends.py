from woojoo import db

class Friends(db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get_friends_by_user_id(user_id):
        return Friends.query.filter(
            Friends.user_id==user_id
        ).all()
        
    @staticmethod
    def get_friend_one(user_id, friend_id):
        return Friends.query.filter(
            (Friends.user_id==user_id) & (Friends.friend_id==friend_id)
        ).first()
    
    @staticmethod
    def insert_friend(user_id, friend_id):
        db.session.add(Friends(
            user_id=user_id,
            friend_id=friend_id,
        ))
        db.session.commit()
        
class Block(db.Model):
    __tablename__ = "block"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get_block_by_user_id(user_id):
        return Block.query.filter(
            Block.user_id==user_id
        ).all()
        
    @staticmethod
    def get_block_one(user_id, friend_id):
        return Block.query.filter(
            (Block.user_id==user_id) & (Block.friend_id==friend_id)
        ).first()
    
    @staticmethod
    def insert_block(user_id, friend_id):
        db.session.add(Block(
            user_id=user_id,
            friend_id=friend_id,
        ))
        db.session.commit()
from woojoo import db
from datetime import datetime
from datetime import timedelta
from pytz import timezone

class TodaysGames(db.Model):
    __tablename__ = "todays_games"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    game = db.Column(db.String(40), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, index=True)
    
    @staticmethod
    def create_todays_game(user_id, game, introduction):
        KST = timezone('Asia/Seoul')
        create_time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(TodaysGames(
            user_id=user_id, 
            game=game, 
            introduction=introduction,
            create_time=create_time
        ))
        db.session.commit()

    @staticmethod
    def get_todays_game_all():
        KST = timezone('Asia/Seoul')
        today = datetime.now().astimezone(KST).strftime('%Y-%m-%d')
        tomorrow = datetime.now() + timedelta(days=1)
        
        return TodaysGames.query.filter(
            TodaysGames.create_time.between(today, tomorrow)
        ).order_by(TodaysGames.create_time.desc()).all()
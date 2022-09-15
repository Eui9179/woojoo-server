from woojoo import db

class UserGames(db.Model):
    __tablename__ = "user_games"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    game = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    nickname = db.Column(db.String(30, 'utf8mb4_unicode_ci'), nullable=True)

    @staticmethod
    def get_games_by_user_id(user_id):
        return UserGames.query.filter(
            UserGames.user_id==user_id
        ).all()
    
    @staticmethod
    def get_game_one_by_user_id(user_id, game):
        return UserGames.query.filter(
            (UserGames.user_id==user_id) & (UserGames.game==game)
        ).one_or_none()
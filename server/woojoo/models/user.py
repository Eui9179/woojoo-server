from woojoo import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name = db.Column(db.String(30, 'utf8mb4_unicode_ci'), nullable=False)
    phone_number = db.Column(db.String(30, 'utf8mb4_unicode_ci'), nullable=False)
    profile_image_name = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=True)
    fcm_token = db.Column(db.String(300), nullable=True)

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter(
            User.id == id
        ).one_or_none()

    @staticmethod
    def get_user_by_phone_number(phone_number):
        return User.query.filter(
            User.phone_number == phone_number
        ).one_or_none()
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "profile_image_name":self.profile_image_name,
        }
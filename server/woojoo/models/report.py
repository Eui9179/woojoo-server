from woojoo import db

class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id = db.Column(db.Integer, nullable=False)
    reported_user_id = db.Column(db.Integer, nullable=False)
    report_numbers = db.Column(db.String(100), nullable=False)
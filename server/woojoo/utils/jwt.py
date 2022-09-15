from flask_jwt_extended import (
    create_access_token,
)
import datetime

class JwtToken:
    def __init__(self, identity):
        self.access_token = create_access_token(identity=identity, expires_delta=False)
    
    def set_refresh_token_expire(self, resp, days=365):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=days) 
        resp.set_cookie(
            'refresh_token_cookie', 
            value=self.refresh_token, 
            expires=expire_date, 
            httponly=True
        )
        
        return resp
        
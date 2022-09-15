from threading import Thread
from flask import Blueprint

from woojoo.controllers.game.todays_game import changeKorGameName

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

from woojoo.controllers.admin.report import *
import requests, json

@admin_bp.route('/fcm-test')
def test_fcm():
    thread = Thread(
        target=send_notification, 
        args=('eIBECDFaQKKysTmJa9-MeQ:APA91bERKYH6eZ8pPBahL6PJ54IvWca0qnuyOilsg2Pxqtqyjcvt6Xrp8nerj5ELmmkENn0d3uZeN1yOyHolm_UYuiijQCbdYMw59mlHN2cGpj33qtYNdL0-PFl3CZ3hGA5-qOEILEF8', 
              'test', 'test', 'ㄱㄱ')
    )
    
    thread.daemon = True
    thread.start()
    
    # dict = {
    #     'to' : 'eIBECDFaQKKysTmJa9-MeQ:APA91bERKYH6eZ8pPBahL6PJ54IvWca0qnuyOilsg2Pxqtqyjcvt6Xrp8nerj5ELmmkENn0d3uZeN1yOyHolm_UYuiijQCbdYMw59mlHN2cGpj33qtYNdL0-PFl3CZ3hGA5-qOEILEF8',
    #     'priority' : 'high', 
    #     'notification' : {
    #         'title' : '님의 오늘의 게임',
    #         'body' : 'sadsad'
    #     }
    # }
    # res = requests.post('https://fcm.googleapis.com/fcm/send',headers=header, data=json.dumps(dict))

    return response_json_with_code()

header = {
        'Content-Type': 'application/json; chearset=utf-8',
        'Authorization':'key=AAAA5YBAC-M:APA91bEJI3-JRSLzrKYoqbj9DJ_f7mbAdhLa-n-2SKEaqtrrcXbCezbQgBG5IBrZ7JQKfUjD8px4GSPaWmWkgaJfV8eC7eGDAFMdndzn-NW8Z7cdvGHZBin7G4jLklGNwWOFaGrdXpUc'
    }

def send_notification(fcm_tokens, name, game, introduction):

    dict = {
        'to' : fcm_tokens,
        'priority' : 'high', 
        'notification' : {
            'title' : '님의 오늘의 게임',
            'body' :  'sdasd'
        }
    }
    res = requests.post('https://fcm.googleapis.com/fcm/send',headers=header, data=json.dumps(dict))
    print(res.status_code)
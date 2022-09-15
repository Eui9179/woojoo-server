from flask import jsonify, make_response

def response_json_with_code(res_code=200, **kwargs):
    return make_response(jsonify(kwargs), res_code)
from flask import request, url_for, redirect
def validated_user ():
    if "id" in request.cookies:
        return True
    else:
        return False

def userID():
    if "id" in request.cookies:
        return request.cookies["id"]
    else:
        return False
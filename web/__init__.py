from flask import Flask
from .flash_toastr import Toastr
from os import path
from .elip import start

def start2():
    return start()

def create_app():
    app =  Flask(__name__)
    toastr = Toastr(app)
    app.config['SECRET_KEY'] = 'idontcare'
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    return app
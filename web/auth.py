from flask import Blueprint, render_template, redirect, url_for, request, flash
from .elip import *

auth = Blueprint("auth", __name__)

@auth.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('action') == 'encode':
            galoa = int(request.form.get('galoa'))
            message = request.form.get('message')
            a = int(request.form.get('a'))
            b = int(request.form.get('b'))
            k1 = int(request.form.get('k1'))
            elip = createElipCurve(galoa, a, b)
            return render_template("home.html", galoa = galoa, 
                message = message, a = a, b = b, elip = elip, 
                k1 = k1, k2 = "", len = elip.order-1, enc  = "",
                message2 = "", leng = int((elip.order-1)/13)+1)      

        elif request.form.get('action') == 'decode':
            id_list = request.form.getlist("checkID")
            galoa = int(request.form.get('galoa'))
            message = request.form.get('message')
            a = int(request.form.get('a'))
            b = int(request.form.get('b'))
            k1 = int(request.form.get('k1'))
            k2 = int(request.form.get('k2'))
            elip = createElipCurve(galoa, a, b)
            ind = -1
            if (id_list == [] or len(id_list) > 1) and request.form.get('messager') == "":
                flash("Musíte vybrat pouze jeden bod jako bod P", 
                    category = 'error')
                return render_template("home.html", galoa = galoa, 
                    message = message, a = a, b = b, elip = elip, 
                    k1 = k1, k2 = "", len = elip.order-1, enc  = "",
                        message2 = "", leng = int((elip.order-1)/13)+1)
            if id_list == [] or len(id_list) > 1:
                ind = int(request.form.get('messager'))
            points = encode(elip, k1, message, ind)
            mess = decode(elip, points, k2)            
            return render_template("home.html", galoa = galoa, 
                message = message, a = a, b = b, elip = elip, 
                k1 = k1, k2 = k2, len = elip.order-1, enc = ind,
                message2 = mess, leng = int((elip.order-1)/13)+1)
    return render_template("home.html", galoa = "", 
                message = "", a = "", b = "", elip = "", 
                k1 = "", k2 = "", len = 0, enc = "",
                message2 = "", leng = 0)

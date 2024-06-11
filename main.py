import flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
import os
import traceback
import urllib.request
import json
import random
from pogoda import *
from register import *
import datetime

# Inicjalizacjia
app = Flask(
    __name__,

    # Gdzie znajduja sie tempalty
    template_folder='templates',

    # Gdzie znajduja sie style
    static_folder='static',
)

app.secret_key = os.urandom(12)

def test2():
  return "hej hej hej razy "

# ładowanie template'u z html
@app.route('/strona_startowa')
def test3():
  return render_template('home.html')

# możliwość zwracania tagów html

@app.route('/kalkulator')
def kalkulator():
  return render_template('kalkulator.html')

# możliwość zwracania tagów html
@app.route('/hej')
def test4():
  return "<h1> hej hej <h1> <br> <ul> <li> raz </li> <li> dwa </li> </ul> </br>"

# przekazywanie parametrow
@app.route('/powitanie/<name>')
def powitaj(name):
  return "Witaj" + " " + str(name)


# Zapisywanie do pliku
filename_powitanie = "powitania.txt"


@app.route('/powitanie_zapis/<imie>')
def powitanie(imie):
  with open(filename_powitanie, "a") as writer:
    now = datetime.datetime.now()
    writer.writelines(imie + "," + str(now) + "\n")
  return "Witaj" + " " + str(imie)

@app.route('/mnozenie/<int:a>/<int:b>')
def mnozenie(a,b):

  mnozenie = a*b
  return "Wynik mnożenia" + " " + str(mnozenie)

# Proste przechwytywanie sesji
@app.route('/loguj_sesja')
def template_sesja():
  # session["logged_in"] = True
  session['logged_in'] = False
  if session.get("logged_in"):
    return render_template("frontpage.html")
  else:
    return "Uzytkownik niezalogowany"

# Wylogowywanie
@app.route('/loguj_wyloguj')
def template_loguj_wyloguj():
    session['logged_in'] = True
    if session.get("logged_in"):
        return render_template("frontpage2.html")
    else:
        return "Uzytkownik niezalogowany"

# Ścieżka taka sama jak w template po a href
@app.route('/wyloguj')
def wyloguj():
    session['logged_in'] = False
    return "Wylogowano"

# Logowanie z formularzem, input - miejsce, gdzie uzytkownik coś wpisuje w formularzu
# w template w form action podajemy link, który mówi co się stanie jak kliknę przycisk submit

@app.route('/logowanie_z_formularzem')
def logowanie_z_folmularzem():
    return render_template('logowanie.html')

# @app.route('/login', methods=["POST"])
# def login_user():
#   if request.form['password'] == "password" and request.form[
#       'username'] == "user":
#     session["logged_in"] = True
#     return render_template("frontpage.html")
#   else:
#     flash("wrong password")
#     return render_template("logowanie.html")

# Rejestracja użytkownika
@app.route('/signup')
def return_registrationpage():
  return render_template('signup.html')



@app.route('/register', methods=["POST"])
def do_register():
  POST_USERNAME = str(request.form['username'])
  POST_PASSWORD = str(request.form['password'])
  #spr. czy podana długość hasła przy rejestracji jest niemniejsza niż 8 znaków.
  sqlsession = return_sqlalchemysession()
  user = User(POST_USERNAME, POST_PASSWORD)
  if len(POST_PASSWORD) < 8:
      return "Hasło musi mieć więcej niż 8 znaków"
  else:
    sqlsession.add(user)
    sqlsession.commit()
    sqlsession.close()
    return test3()

#Interaktywne logowanie
@app.route('/home')
def home():
  if not session.get('logged_in'):
    return render_template('logowanie.html')
  else:
    return render_template('frontpage2.html')


@app.route('/login', methods=["POST"])
def login_user_extended():
  POST_USERNAME = str(request.form['username'])
  POST_PASSWORD = str(request.form['password'])

  #Stworz obiekt sesji SQLalchemy (ORM)
  sqlsession = return_sqlalchemysession()

  # Zadaj zapytanie w sposob bezpieczny
  # od sqlinjection
  # query = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]))
  query = sqlsession.query(User).filter(User.username == POST_USERNAME)

  #wez 1 uzytkownika z takim nickiem (zakladamy ze nie ma powtorek)
  user = query.first()
  try:
    #Ta linia musi być w try, bo jeżeli nie ma usera (user==None) to nie zadziała user.check_password

    if user.password == POST_PASSWORD:
      session['logged_in'] = True
      # return render_template('frontpage.html')

    else:
      # Jak działa flash: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
      flash('No user or wrong password provided')
      return render_template('logowanie.html')
  except AttributeError as e:
    flash('No user or wrong password provided')
    #traceback trick to printout the error despite the except
    print(traceback.format_exc())

  return home()

@app.route('/miasto')
def miasto():
    return render_template('miasto.html')

@app.route('/pogoda_zapis/<miasto>')
def zapisz_pogode(miasto):
    temp, humid, weathertype, rain = pobierzpogode(miasto)
    with open(f"{miasto}.txt", "w") as writer:
        writer.write(f"Miasto: {miasto} \n Temperatura: {temp} \n Wilgotność: {humid} \n Typ pogody: {weathertype} \n Deszcz {rain} \n")
    return jsonify({"status": "success", "message": f"Pogoda dla {miasto} została zapisana."})

@app.route("/pogoda/<miasto>", methods=["GET"])
def pokazpogode(miasto):
    try:
        temp, humid, weathertype, rain = pobierzpogode(miasto)
        return render_template("pogoda.html",
                             miasto=miasto,
                             temp=temp,
                             humid=humid,
                             weathertype=weathertype,
                             rain=rain)
    except Exception:
        flash('Nie istnieje miasto o takiej nazwie!')
        return render_template("miasto.html", username=session['username'])

if __name__ == "__main__":
  app.run()

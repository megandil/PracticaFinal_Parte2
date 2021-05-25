from flask import Flask, render_template,abort
import os
import json
import requests
app = Flask(__name__)
key=os.environ["key"]
@app.route('/')
def inicio():
    return render_template("index.html")
@app.route('/lista',methods=['POST'])
def lista():
    from flask import request
    cad=request.form.get("cadena")
    from urllib import request
    datos = request.urlopen(f"https://steamid.io/lookup/{cad.lower()}")
    from bs4 import BeautifulSoup
    soup =  BeautifulSoup(datos,features="lxml" )
    acum=0
    tags = soup.find_all("img")
    for tag in tags:
        acum=acum+1
        if acum == 6:
            id=tag.get("data-clipboard-text")
    return render_template("lista.html",id=id)
@app.route('/juegos/<id>')
def juegos(id):
    identificacion=id
    juegos=[]
    r=requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&include_played_free_games=1&include_appinfo=True&steamid={identificacion}&format=json")
    datos = r.json()
    for i in datos.get("response").get("games"):
        dic={"juego":i.get("name"),"id":i.get("appid"),"img":i.get("img_logo_url")}
        juegos.append(dic)
    return render_template("juegos.html",juegos=juegos)

@app.route('/recientes/<id>')
def recientes(id):
    identificacion=id
    recientes=[]
    r=requests.get(f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={identificacion}&format=json")
    datos = r.json()
    for i in datos.get("response").get("games"):
        dic={"juego":i.get("name"),"id":i.get("appid"),"img":i.get("img_logo_url")}
        recientes.append(dic)
    return render_template("recientes.html",recientes=recientes)
@app.route('/infocuenta/<id>')
def infocuenta(id):
    identificacion=id
    info=[]
    r=requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={identificacion}")
    datos = r.json()
    for i in datos.get("response").get("players"):
        info.append(i.get("steamid"))
        info.append(i.get("realname"))
        info.append(i.get("loccountrycode"))
    return render_template("infocuenta.html",info=info)
@app.route('/juego/<idjuego>')
def infojuego(idjuego):  
    idgame=idjuego
    infojuego=[]
    r=requests.get(f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={idgame}&count=3&maxlength=300&format=json")
    datos = r.json()
    for i in datos.get("appnews").get("newsitems"):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(i.get("contents"))
        dic={"titulo":i.get("title"),"contenido":soup.get_text()}
        infojuego.append(dic) 
    return render_template("infojuego.html",infojuego=infojuego)

app.run('0.0.0.0',5000, debug=True)
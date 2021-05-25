import json
import requests
import os
import urllib
from urllib import request
def nombre_id(nombre):
    if len(nombre) == 0:
        nombre="megadani1020"
    datos = request.urlopen(f"https://steamid.io/lookup/{nombre.lower()}")
    from bs4 import BeautifulSoup
    soup =  BeautifulSoup(datos,features="lxml" )
    acum=0
    tags = soup.find_all("img")
    for tag in tags:
        acum=acum+1
        if acum == 6:
            id=tag.get("data-clipboard-text")
    return id
def juegos_obtiene(key,id):
    juegos=[]
    r=requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&include_played_free_games=1&include_appinfo=True&steamid={id}&format=json")
    datos = r.json()
    for i in datos.get("response").get("games"):
        juegos.append(i.get("name"))
    return juegos
def juegos_recientes(key,id):
    recientes=[]
    r=requests.get(f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={id}&format=json")
    datos = r.json()
    for i in datos.get("response").get("games"):
        recientes.append(i.get("name"))
    return recientes
def info_user(key,id):
    info=[]
    r=requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id}")
    datos = r.json()
    for i in datos.get("response").get("players"):
        info.append(i.get("steamid"))
        info.append(i.get("realname"))
        info.append(i.get("loccountrycode"))
    return info
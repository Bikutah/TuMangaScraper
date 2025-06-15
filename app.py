from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/todos")
def todos():
    page = request.args.get("page", "1")
    url = f"https://lectortmo.com/library?_pg=1&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    resultados = []
    for card in soup.select("div[class*=element]"):
        titulo_tag = card.select_one("h4")
        link_tag = card.select_one("a")
        thumbnail_div = card.select_one("div.thumbnail")
        style_tag = thumbnail_div.select_one("style") if thumbnail_div else None

        if not titulo_tag or not link_tag:
            continue

        titulo = titulo_tag.text.strip()
        link = link_tag["href"].strip()

        # Obtener imagen desde el <style> con background-image
        imagen = None
        if style_tag and style_tag.string:
            match = re.search(r"url\('([^']+)'\)", style_tag.string)
            if match:
                imagen = match.group(1)

        print(url)

        resultados.append({
            "titulo": titulo,
            "link": link,
            "imagen": imagen
        })
    
    print(res)

    return jsonify({
        "pagina": page,
        "mangas": resultados
    })

@app.route("/buscar")
def buscar():
    query = request.args.get("q", "")
    page = request.args.get("page", "1")

    url = f"https://lectortmo.com/library?title={query.replace(' ', '+')}&_pg=1&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    resultados = []
    for card in soup.select("div[class*=element]"):
        titulo_tag = card.select_one("h4")
        link_tag = card.select_one("a")
        thumbnail_div = card.select_one("div.thumbnail")
        style_tag = thumbnail_div.select_one("style") if thumbnail_div else None

        # Si falta alguno de los elementos necesarios, salteamos
        if not titulo_tag or not link_tag:
            continue

        titulo = titulo_tag.text.strip()
        link = link_tag["href"].strip()

        # Extraer imagen desde el <style>
        imagen = None
        if style_tag and style_tag.string:
            match = re.search(r"url\('([^']+)'\)", style_tag.string)
            if match:
                imagen = match.group(1)

        print(url)

        resultados.append({
            "titulo": titulo,
            "link": link,
            "imagen": imagen
        })

    print(res)

    return jsonify({
        "query": query,
        "pagina": page,
        "resultados": resultados
    })


if __name__ == "__main__":
    app.run()

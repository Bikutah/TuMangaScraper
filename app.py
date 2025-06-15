from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/buscar")
def buscar():
    query = request.args.get("q", "")
    url = f"https://lectortmo.com/library?title={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    resultados = []
    for card in soup.select("div.element"):
        titulo = card.select_one("h4").text.strip()
        link = "https://lectortmo.com" + card.select_one("a")["href"]
        imagen = card.select_one("img")["data-src"]
        resultados.append({
            "titulo": titulo,
            "link": link,
            "imagen": imagen
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()

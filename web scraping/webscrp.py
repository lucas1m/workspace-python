# import scraping
from bs4 import BeautifulSoup
import requests

# import flask RestFull
import os
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)
app.debug = True


@app.route('/temp/<string:city>', methods=['GET'])
def jsonreturn(city):

    # Requests
    html = requests.get("https://www.tempo.com/" + city.lower() + ".htm").content
    soup = BeautifulSoup(html, 'html.parser')

    # find by class HTML
    temperatura = soup.find("span", class_="dato-temperatura changeUnitT")
    tempfinal = temperatura.string

    print(city)
    print(tempfinal)

    #retorno em json
    return jsonify(
    {'Api':
        {
        'Cidade':city,
        'Temperatura':tempfinal
        }
    })

@app.route('/cot/<string:moeda>', methods=['GET'])
def dolreturn(moeda):
    
    html = request.get("https://economia.uol.com.br/cotacoes/").content
    soup = BeautifulSoup(html, 'html.parser')

    dolar = soup.find("span", class_="")

    return 'Oks'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')   # ip geral
from flask import Flask, json, jsonify, render_template
import mysql.connector
from flask import request
import requests
import json
from datetime import datetime
from unidecode import unidecode

'''
Código consumido em flutter, no qual realiza um POST com informações de cadastro do produto

llopes
'''

app = Flask(__name__)

#CONEXAO BANCO MYSQ-LOCAL
def conexao():

    config = {
    'host':'localhost',
    'port':'3306',
    'user':'root',
    'password':'YourPass',
    'database':'YourDatabase'
    }

    conn = mysql.connector.connect(**config)
    return conn 

def MontaBody(array_products):

    conex = conexao()
    cursor = conex.cursor()
    
    codigo = array_products[0]
    descri = array_products[1]
    valor  = array_products[2]
    um     = array_products[3]
    dtcad  = array_products[4]
    
    cQuery = "INSERT INTO totvs.produtos VALUES ('"+codigo+"', '"+descri+"', '"+valor+"', '"+um+"', '"+dtcad+"' )"
    cursor.execute(cQuery)
    conex.commit()

    return jsonify({'Api':'Insert completo'})

@app.route('/', methods=['GET'])
def get():
    return jsonify({'Api-REST':'No ar'})

@app.route('/post', methods=['POST'])
def post():
    tdOK = True # Manipular após cadastro

    js = request.get_data()
    data = json.loads(js)
    print()
    print(data)
    print()

    array_products = [] #Array com info dos produtos para post no workbench

    if request.method == 'POST':

        array_products.append(data['codigo'])   # codigo
        array_products.append(data['descri'])   # descri
        array_products.append(data['valor'])    # valor
        array_products.append(data['um'])       # um
        array_products.append(data['dtcad'])

        MontaBody(array_products)

        if tdOK:
            return jsonify({'api_produto'
                                'Return':'Success'})
        else:
            return jsonify({'api_produto'
                                'Return':'Error!'})

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='80')
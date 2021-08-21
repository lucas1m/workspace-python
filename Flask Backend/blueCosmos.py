from flask import Flask, json, jsonify
import mysql.connector
import requests
import json

app = Flask(__name__)

'''

Código semelhante ao rotas, entretanto, neste caso nós consumimos uma API publica na qual retorna toda informação de um produto,
a partir de seu NCM.
Construido codigo em Flutter no qual realiza a leitura de um codigo de barras e faz um post na rota deste codigo Flask
já inserindo no banco com os dados retornados do BlueCosmos

llopes
'''

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

@app.route('/getproducts/<string:ean>', methods=['POST'])
def getproduct(ean):

    conex = conexao()
    cursor = conex.cursor()

    token = 'YourTokenApi' # é gratuito, relaxa! Basta criar um breve cadastro em bluecosmos
    headers = {
          'X-Cosmos-Token': token,
          'Content-Type': 'application/json',
          'User-Agent': 'Cosmos-API-Request'
      }

    req      = requests.get('https://api.cosmos.bluesoft.com.br/gtins/' + ean + '.json', headers = headers)
    data = json.loads(req.text)

    gtin = data['gtin']
    descri   = data['description']
    precomin = data['price']
    precomax = data['max_price']
    cod_ncm = data['ncm']['code']
    desc_ncm = data['ncm']['full_description']

    tamdesc = len(desc_ncm)
    descrimax = 0

    #garante integridade para não causar estouro de campo na descrição
    if tamdesc > 254:
        descrimax = 254
    else:
        descrimax = tamdesc

    #inserção e commit no banco
    cQuery = "INSERT INTO totvs.prodNCM VALUES ('"+str(gtin)+"', '"+descri+"', '"+precomin+"', '"+str(precomax)+"', '"+cod_ncm+"','"+desc_ncm[0:descrimax]+"' )"
    cursor.execute(cQuery)
    conex.commit()

    return jsonify(
        {
        'Produto':
        {
            'gtin':gtin,
            'Descricao':descri,
            'PrecoMin':precomin,
            'PrecoMax':precomax,
            'NCM':cod_ncm,
            'Descri_NCM':desc_ncm
        },
        'Status':'Produto Cadastrado!'
        }
    )

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='80', debug=True)
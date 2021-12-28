from typing import ClassVar
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app)

from products import products


@app.route('/ping')
def ping():
    return jsonify({"message":"pong!"})

@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify(products)

@app.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    productsfound = [product for product in products if product['name']== product_name]
    if (len(productsfound)>0):
        return jsonify({'product':productsfound[0]})
    return jsonify({'Message': 'Producto no encontrado'})

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name":request.json['name'],
        "price":request.json['price'],
        "quantity":request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message":"Producto agregado","products":products})

# ----------------------- INICIO DE RUTAS PARA EL PROYECTO---------------------------------

@app.route('/Reporte1', methods = ['POST'])
def Reporte1():
    VariablesParam = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2']
    }

    mivar = VariablesParam['Variable1']
    mivar2 = VariablesParam['Variable2']
    print(VariablesParam)
    print("mi variable 1 es")
    print(mivar)
    print("mi variable 2 es")
    print(mivar2)
    print("EL TIPO DE ARCHIVO ES")
    print(tipo)
    print("el archivo")
    print(dataset.shape)
    print(dataset.head())
    print(dataset.describe())
    #dataset.plot(x='Hours', y='Scores', style='o')
    #plt.title('Hours vs Percentage')
    #plt.xlabel('Hours Studied')
    #plt.ylabel('Percentage Score')
    #plt.show()
    


    respuesta = jsonify({"message":"variables recibidas"})
    return respuesta

@app.route('/CargarArchivo', methods = ['POST'])
def Carga():
    global Archivo, dataset, tipo
    Archivo = request.files['files']
    filename = secure_filename(Archivo.filename)
    extension = os.path.splitext(filename)
    print(extension[1])
    if extension[1] == ".csv":
        dataset = pd.read_csv(Archivo)
        tipo = 1
    elif extension[1] == ".xlsx":
        dataset = pd.read_excel(Archivo)
        tipo = 2
    elif extension[1] == ".json":
        dataset = pd.read_json(Archivo)
        tipo = 3
    
    return jsonify({"message":"ARCHIVO RECIBIDO"})



if __name__ == '__main__':
    app.run(debug = True, port=4000)



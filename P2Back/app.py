from typing import ClassVar
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from pandas.core.construction import array
from werkzeug.utils import secure_filename

from sklearn import base, datasets, linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import base64

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

@app.route('/GetReporte1', methods=['GET'])
def getReporte1():
    with open ("Reporte1.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),"pais":R1_pais})


@app.route('/Reporte1', methods = ['POST'])
def Reporte1():
    global R1_pais, R1_Col_Pais, R1_Col_Fecha, R1_Col_Confirmados, R1_Grado_Polinomio, R1_rmse, R1_r2
    VariablesParam = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
    }
    R1_pais = VariablesParam['Variable1']
    R1_Col_Pais = VariablesParam['Variable2']
    R1_Col_Fecha = VariablesParam['Variable3']
    R1_Col_Confirmados = VariablesParam['Variable4']

    if R1_pais == '':
        Datos = pd.DataFrame(dataset)
        Ejex = Datos[R1_Col_Fecha]
        Ejey = Datos[R1_Col_Confirmados]

        X = pd.to_datetime(Ejex).astype(np.int64)
        X = X[:,np.newaxis]
        Y = Ejey[:,np.newaxis]
        plt.scatter(Ejex,Y)

        R1_Grado_Polinomio = 3
        Caracteristicas_Polinomio = PolynomialFeatures(degree=R1_Grado_Polinomio)
        Transform_x = Caracteristicas_Polinomio.fit_transform(X)
        modelo = linear_model.LinearRegression().fit(Transform_x,Y)

        nueva_y = modelo.predict(Transform_x)

        R1_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
        R1_r2 = r2_score(Y,nueva_y)
        print('RMSE: ', R1_rmse)
        print('R2: ', R1_r2)

        plt.plot(Ejex, Y, color='coral', linewidth=3)
        plt.grid()
        Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R1_Grado_Polinomio, round(R1_rmse,2), round(R1_r2,2))
        plt.title("Tendencia de la Infeccion por Covid-19 en un país\n " + Titulo, fontsize=10)
        plt.savefig("Reporte1.png")
    else:
        Datos = dataset.loc[dataset[R1_Col_Pais]==R1_pais]
        Datos = pd.DataFrame(Datos)
        Ejex = Datos[R1_Col_Fecha]
        Ejey = Datos[R1_Col_Confirmados]

        X = pd.to_datetime(Ejex).astype(np.int64)
        X = X[:,np.newaxis]
        Y = Ejey[:,np.newaxis]
        plt.scatter(Ejex,Y)

        R1_Grado_Polinomio = 3
        Caracteristicas_Polinomio = PolynomialFeatures(degree=R1_Grado_Polinomio)
        Transform_x = Caracteristicas_Polinomio.fit_transform(X)
        modelo = linear_model.LinearRegression().fit(Transform_x,Y)

        nueva_y = modelo.predict(Transform_x)

        R1_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
        R1_r2 = r2_score(Y,nueva_y)
        print('RMSE: ', R1_rmse)
        print('R2: ', R1_r2)

        plt.plot(Ejex, Y, color='coral', linewidth=3)
        plt.grid()
        Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R1_Grado_Polinomio, round(R1_rmse,2), round(R1_r2,2))
        plt.title("Tendencia de la Infeccion por Covid-19 en un país\n " + Titulo, fontsize=10)
        plt.savefig("Reporte1.png")

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta


@app.route('/Reporte2', methods = ['POST'])
def Reporte2():
    global R2_pais, R2_Col_pais, R2_Col_Infectados, R2_Col_Dias, R2_prediccion
    VariablesParamR2 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R2_pais = VariablesParamR2['Variable1']
    R2_Col_pais = VariablesParamR2['Variable2']
    R2_Col_Dias= VariablesParamR2['Variable3']
    R2_Col_Infectados = VariablesParamR2['Variable4']
    R2_prediccion = VariablesParamR2['Variable5']
    R2_prediccion = float(R2_prediccion)    

    Datos = dataset.loc[dataset[R2_Col_pais]==R2_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R2_Col_Infectados]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R2_Grado_Polinomio = 4
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R2_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R2_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R2_r2 = r2_score(Ejey,nueva_y)
    print('RMSE: ', R2_rmse)
    print('R2: ', R2_r2)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R2_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R2_Grado_Polinomio, round(R2_rmse,2), round(R2_r2,2))
    plt.title("Prediccion de Infectados en un país\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte2.png")
    plt.show()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta


@app.route('/Reporte4', methods = ['POST'])
def Reporte4():
    global R4_departamento, R4_Col_departamento, R4_Col_muertes, R4_Col_Dias, R4_prediccion
    VariablesParamR2 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R4_departamento = VariablesParamR2['Variable1']
    R4_Col_departamento = VariablesParamR2['Variable2']
    R4_Col_Dias= VariablesParamR2['Variable3']
    R4_Col_muertes = VariablesParamR2['Variable4']
    R4_prediccion = VariablesParamR2['Variable5']
    R4_prediccion = float(R4_prediccion)    

    Datos = dataset.loc[dataset[R4_Col_departamento]==R4_departamento]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R4_Col_muertes]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R4_Grado_Polinomio = 4
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R4_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R4_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R4_r2 = r2_score(Ejey,nueva_y)
    print('RMSE: ', R4_rmse)
    print('R2: ', R4_r2)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R4_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R4_Grado_Polinomio, round(R4_rmse,2), round(R4_r2,2))
    plt.title("Prediccion de mortalidad por COVID en un departamento\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte4.png")
    plt.show()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta


@app.route('/Reporte5', methods = ['POST'])
def Reporte5():
    global R5_pais, R5_Col_pais, R5_Col_muertes, R5_Col_Dias, R5_prediccion
    VariablesParamR2 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R5_pais = VariablesParamR2['Variable1']
    R5_Col_pais = VariablesParamR2['Variable2']
    R5_Col_Dias= VariablesParamR2['Variable3']
    R5_Col_muertes = VariablesParamR2['Variable4']
    R5_prediccion = VariablesParamR2['Variable5']
    R5_prediccion = float(R5_prediccion)    

    Datos = dataset.loc[dataset[R5_Col_pais]==R5_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R5_Col_muertes]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R5_Grado_Polinomio = 4
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R5_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R5_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R5_r2 = r2_score(Ejey,nueva_y)
    print('RMSE: ', R5_rmse)
    print('R2: ', R5_r2)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R4_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R5_Grado_Polinomio, round(R5_rmse,2), round(R5_r2,2))
    plt.title("Prediccion de mortalidad por COVID en un departamento\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte5.png")
    plt.show()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/Reporte9', methods = ['POST'])
def Reporte9():
    global R9_pais, R9_col_pais, R9_col_vacunacion, R9_col_dias
    regr = linear_model.LinearRegression()
    VariablesParamR2 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }
    R9_pais = VariablesParamR2['Variable1']
    R9_col_pais = VariablesParamR2['Variable2']
    R9_col_vacunacion= VariablesParamR2['Variable3']
    R9_col_dias= VariablesParamR2['Variable4']

    Datos = dataset.loc[dataset[R9_col_pais]==R9_pais]
    Datos = pd.DataFrame(Datos)

    Ejex = Datos[R9_col_dias]

    y = Datos[R9_col_vacunacion]
    X = pd.to_datetime(Ejex).astype(np.int64)
    X = X[:,np.newaxis]
    regr.fit(X,y)
    m = regr.coef_[0]
    b = regr.intercept_
    y_p = regr.predict(X)
    plt.scatter(X,y, color = 'black')
    plt.plot(X,y_p,color = 'blue')
    r2 = r2_score(y,y_p)
    rmse = np.sqrt(mean_squared_error(y, y_p))
    Titulo = 'Ecuación: Y = {}*x + {}; RMSE = {}; R2 = {}'.format(m,b, round(rmse,2), r2)
    plt.title("Prediccion de mortalidad por COVID en un departamento\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte9.png")
    plt.show()



@app.route('/CargarArchivo', methods = ['POST'])
def Carga():
    global Archivo, dataset, tipo
    Archivo = request.files['files']
    filename = secure_filename(Archivo.filename)
    extension = os.path.splitext(filename)
    print(extension[1])
    if extension[1] == ".csv":
        dataset = pd.read_csv(Archivo,header = 0,encoding='latin-1')
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



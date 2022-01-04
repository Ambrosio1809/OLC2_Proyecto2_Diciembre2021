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

    if R1_Coeficiente[3] > 0:
        Conclusion = 'Debido a que la grafica muestra una pendiente positiva, nos indica que \n la tendencia de la infección del Covid-19 aumentara conforme pase el tiempo'
    else:
        Conclusion = 'Debido a que la grafica muestra una pendiente negativa, esto nos indica que \n la tendencia de la infección del Covid-19 disminuira conforme pase el tiempo'

    with open ("Reporte1.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R1_pais,
                    "grado": R1_Grado_Polinomio, 
                    "RMSE":R1_rmse,
                    "R2": R1_r2,
                    "conclusion":Conclusion})

@app.route('/Reporte1', methods = ['POST'])
def Reporte1():
    global R1_pais, R1_Col_Pais, R1_Col_Fecha, R1_Col_Confirmados, R1_Grado_Polinomio, R1_rmse, R1_r2, R1_Coeficiente
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
        R1_Coeficiente = modelo.coef_[0]
        print(R1_Coeficiente)
        R1_r2 = r2_score(Y,nueva_y)
        print('RMSE: ', R1_rmse)
        print('R2: ', R1_r2)

        plt.plot(Ejex, Y, color='coral', linewidth=3)
        plt.grid()
        Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R1_Grado_Polinomio, round(R1_rmse,2), round(R1_r2,2))
        plt.title("Tendencia de la Infeccion por Covid-19 en un país\n " + Titulo, fontsize=10)
        plt.savefig("Reporte1.png")
        plt.close()
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
        R1_Coeficiente = modelo.coef_[0]
        R1_r2 = r2_score(Y,nueva_y)

        plt.plot(Ejex, Y, color='coral', linewidth=3)
        plt.grid()
        Titulo = 'Grado = {}; RMSE = {}; R2 = {}'.format(R1_Grado_Polinomio, round(R1_rmse,2), round(R1_r2,2))
        plt.title("Tendencia de la Infeccion por Covid-19 en un país\n " + Titulo, fontsize=10)
        plt.savefig("Reporte1.png")
        plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte2', methods=['GET'])
def getReporte2():
    if R2_r2 > 0.75:
        Conclusion = 'Debido a que nuestro coeficiente de correlacion parece estar en un valor\n cercano a 1, podemos indicar que los datos y nuestra predicción se ajustan relativamente \nexactos a la prediccion realizada'
    else:
        Conclusion = 'Debido a que nuestro coeficiente de correlacion parece no estar en un valor\n cercano a 1, podemos indicar que los datos y nuestra predicción no se ajustan \ncorrectamente a la prediccion realizada'

    with open ("Reporte2.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R2_pais,
                    "grado": R2_Grado_Polinomio, 
                    "RMSE":round(R2_rmse,4),
                    "R2": round(R2_r2,4),
                    "Dias":R2_prediccion,
                    "Prediccion":round(R2_pred,4),
                    "Conclusion":Conclusion})

@app.route('/Reporte2', methods = ['POST'])
def Reporte2():
    global R2_pais, R2_Col_pais, R2_Col_Infectados, R2_Col_Dias, R2_prediccion,R2_Grado_Polinomio, R2_rmse, R2_r2, R2_pred, R2_Coeficiente
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
    R2_Coeficiente = modelo.coef_
    R2_r2 = r2_score(Ejey,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R2_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R2_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {} \n para {} dias la prediccion es: {}'.format(R2_Grado_Polinomio, round(R2_rmse,2), round(R2_r2,2),R2_prediccion,round(R2_pred,2))
    plt.title("Prediccion de Infectados en un país\n " + Titulo, fontsize=10)
    plt.xlabel('Días')
    plt.ylabel('Infectados')
    plt.savefig("Reporte2.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte3', methods=['GET'])
def getReporte3():
    if R3_m[0] > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion mayor a 1, podemos concluir \nque nuestro indice crecera demasiado rapido conforme al tiempo pase, por lo cual\n la pandemia sera un riesgo mas grande para el mundo'
    elif R3_m[0]< 1 or R3_m[0] > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos indica que\n el indice seguira creciendo pero a un nivel mas constante, no tan rapido\n como si lo fuese mayor a 1'
    elif R3_m[0] < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos concluir\n que conforme el tiempo transcurra la pandemia ira disminuyendo hasta\n que ya no exista más'
    with open ("Reporte3.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "formula": R3_Formula, 
                    "RMSE":round(R3_rmse,4),
                    "R2": round(R3_r2,4),
                    "coef": R3_m[0],
                    "intercept": R3_b[0],
                    "Conclusion": conclusion})

@app.route('/Reporte3', methods = ['POST'])
def Reporte3():
    global R3_col_casos, R3_col_dias, R3_coef,R3_m ,R3_b, R3_Formula, R3_r2, R3_rmse
    VariablesParamR11 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2']
    }
    regr = linear_model.LinearRegression()
    R3_col_casos = VariablesParamR11['Variable1']
    R3_col_dias = VariablesParamR11['Variable2']

    Datos = pd.DataFrame(dataset)
    Ejex = Datos[R3_col_dias]
    Ejey = Datos[R3_col_casos]
    Eje_x =[]

    for i in Datos.index:
        Eje_x.append(i)
    X = np.asarray(Eje_x)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]
    plt.scatter(X,Y)

 
    regr.fit(X,Y)
    R3_coef = regr.coef_
    R3_m = regr.coef_[0]
    R3_b = regr.intercept_
    R3_y_p = regr.predict(X)

    plt.scatter(X,Y,color = 'black')
    plt.plot(X,R3_y_p, color = 'blue')
    R3_Formula = 'y={0}*x+{1}'.format(R3_m[0], R3_b[0])
    R3_r2 = r2_score(Y,R3_y_p)
    R3_rmse = np.sqrt(mean_squared_error(Y,R3_y_p))

    Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R3_Formula, R3_coef, round(R3_rmse,4), round(R3_r2,4))
    plt.title("Indice de Progresión de la pandemia.\n " + Titulo, fontsize=10)
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.savefig("Reporte3.png")
    plt.close()
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte4', methods=['GET'])
def getReporte4():
    if R4_Coeficiente[4] >0:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta\nser positivo, podemos concluir que la mortalidad debido al covid-19 en este\ndepartamento ira aumentando si la pandemia no se logra controlar a tiempo'
    else:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta\nser negativo, podemos concluir que la mortalidad debido al covid-19 en este\ndepartamento ira disminuyendo debido a que probablemente la pandemia fue\ncontrolada'

    with open ("Reporte4.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R4_departamento,
                    "grado": R4_Grado_Polinomio, 
                    "RMSE":round(R4_rmse,4),
                    "R2": round(R4_r2,4),
                    "Dias":R4_prediccion,
                    "Prediccion":round(R4_pred,4),
                    "Conclusion": conclusion})

@app.route('/Reporte4', methods = ['POST'])
def Reporte4():
    global R4_departamento, R4_Col_departamento, R4_Col_muertes, R4_Col_Dias, R4_prediccion, R4_pred, R4_rmse, R4_r2, R4_Grado_Polinomio, R4_Coeficiente
    VariablesParamR4 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R4_departamento = VariablesParamR4['Variable1']
    R4_Col_departamento = VariablesParamR4['Variable2']
    R4_Col_Dias= VariablesParamR4['Variable3']
    R4_Col_muertes = VariablesParamR4['Variable4']
    R4_prediccion = VariablesParamR4['Variable5']
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
    plt.scatter(X,Y)

    R4_Grado_Polinomio = 4
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R4_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R4_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R4_Coeficiente = modelo.coef_
    R4_r2 = r2_score(Ejey,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R4_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R4_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Departamento: {} Grado = {}; RMSE = {}; R2 = {}; \n Con una prediccion para: {} dias de = {} muertes'.format(R4_departamento, R4_Grado_Polinomio, R4_rmse, R4_r2, R4_prediccion,R4_pred)
    plt.title("Prediccion de mortalidad por COVID en un departamento\n " + Titulo, fontsize=10)
    plt.xlim(x_nuevo_min,x_nuevo_max)
    plt.ylim(0,len(Ejey)+100)
    plt.xlabel('Días')
    plt.ylabel('Muertes')
    plt.savefig("Reporte4.png")
    plt.close()
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte5', methods=['GET'])
def getReporte5():
    if R5_Coeficiente[3] >0:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta ser\npositivo, podemos concluir que la mortalidad debido al covid-19 en este pais\nira aumentando si la pandemia no se logra controlar a tiempo'
    else:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta ser\nnegativo, podemos concluir que la mortalidad debido al covid-19 en este pais\nira disminuyendo debido a que probablemente la pandemia fue controlada'
    with open ("Reporte5.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R5_pais,
                    "grado": R5_Grado_Polinomio, 
                    "RMSE":round(R5_rmse,4),
                    "R2": round(R5_r2,4),
                    "Dias":R5_prediccion,
                    "Prediccion":round(R5_pred,4),
                    "Conclusion":conclusion})

@app.route('/Reporte5', methods = ['POST'])
def Reporte5():
    global R5_pais, R5_Col_pais, R5_Col_muertes, R5_Col_Dias, R5_prediccion, R5_Grado_Polinomio, R5_rmse, R5_r2, R5_pred, R5_Coeficiente
    VariablesParamR5 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R5_pais = VariablesParamR5['Variable1']
    R5_Col_pais = VariablesParamR5['Variable2']
    R5_Col_Dias= VariablesParamR5['Variable3']
    R5_Col_muertes = VariablesParamR5['Variable4']
    R5_prediccion = VariablesParamR5['Variable5']
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

    R5_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R5_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R5_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R5_Coeficiente = modelo.coef_
    R5_r2 = r2_score(Ejey,nueva_y)
    x_nuevo_min = 0.0
    x_nuevo_max = R5_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R5_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Pais: {} \n Prediccion para {} dias es de {} muertes \n Grado = {}; RMSE = {}; R2 = {}'.format(R5_pais, R5_prediccion, round(R5_pred,2), R5_Grado_Polinomio, round(R5_rmse,2), round(R5_r2,2))
    plt.title("Prediccion de mortalidad por COVID en un Pais\n " + Titulo, fontsize=10)
    plt.xlabel('Días')
    plt.ylabel('Muertes')
    plt.savefig("Reporte5.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte6', methods=['GET'])
def getReporte6():
    if R6_m > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion es mayor a 1, podemos concluir\nque nuestro numero de muertes por coronavirus crecera demasiado rapido conforme\n al tiempo pase, por lo cual la pandemia sera un riesgo mas grande para el pais'
    elif R6_m< 1 or R6_m > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos indica\nque el numero de muertes seguira creciendo pero a un nivel mas constante,\n no tan rapido como si lo fuese mayor a 1'
    elif R6_m < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos concluir\n que conforme el tiempo transcurra la pandemia ira disminuyendo hasta que\n ya no exista más, por lo cual no existiran muertes por coronavirus'
    with open ("Reporte6.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R6_pais,
                    "formula": R6_Formula, 
                    "RMSE":round(R6_rmse,4),
                    "R2": round(R6_r2,4),
                    "coef": R6_m,
                    "intercept": round(R6_b,2),
                    "Conclusion":conclusion})

@app.route('/Reporte6', methods = ['POST'])
def Reporte6():
    global R6_pais, R6_Col_Pais, R6_Col_muertes, R6_Col_dias, R6_coef, R6_m, R6_b, R6_Formula, R6_r2, R6_rmse
    regr = linear_model.LinearRegression()

    VariablesParamR6 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
    }

    R6_pais = VariablesParamR6['Variable1']
    R6_Col_Pais = VariablesParamR6['Variable2']
    R6_Col_dias = VariablesParamR6['Variable3']
    R6_Col_muertes = VariablesParamR6['Variable4']

    Datos = dataset.loc[dataset[R6_Col_Pais]==R6_pais]
    Datos = pd.DataFrame(Datos)

    Ejex = Datos[R6_Col_dias]
    Ejey = Datos[R6_Col_muertes]
    
    X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(X)
    X = X[:,np.newaxis]

    regr.fit(X,Ejey)
    R6_coef = regr.coef_
    R6_m = regr.coef_[0]
    print(R6_m)
    R6_b = regr.intercept_
    R6_y_p = regr.predict(X)
    plt.scatter(X,Ejey,color = 'black')
    plt.plot(X,R6_y_p, color = 'blue')
    R6_Formula = 'y={0}*x+{1}'.format(R6_m, round(R6_b,2))
    R6_r2 = r2_score(Ejey,R6_y_p)
    R6_rmse = np.sqrt(mean_squared_error(Ejey,R6_y_p))

    Titulo = 'Formula = {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R6_Formula, R6_m, round(R6_rmse,2), round(R6_r2,2))
    plt.title("Análisis del número de muertes por coronavirus en un País.\n " + Titulo, fontsize=10)
    plt.xlabel('Dias')
    plt.ylabel('Muertes')
    plt.savefig("Reporte6.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte7', methods=['GET'])
def getReporte7():
    if R7_Coeficiente[3] >0:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta\nser positivo, podemos concluir que la tendencia de infectados debido al covid-19\n en este pais ira aumentando si la pandemia no se logra controlar a tiempo'
    else:
        conclusion = 'Con nuestra prediccion y además el modelo con un coeficiente que resulta\nser negativo, podemos concluir que la tendencia de infectados debido al covid-19\n en este pais ira disminuyendo debido a que probablemente la pandemia\nfue controlada'
    with open ("Reporte7.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R7_pais,
                    "grado": R7_Grado_Polinomio, 
                    "RMSE":round(R7_rmse,4),
                    "R2": round(R7_r2,4),
                    "Dias":R7_Cant_Dias,
                    "Prediccion":round(R7_pred,4),
                    "Conclusion":conclusion})

@app.route('/Reporte7', methods = ['POST'])
def Reporte7():
    global R7_pais, R7_Col_Pais, R7_Col_Fecha, R7_Col_Confirmados, R7_Grado_Polinomio, R7_rmse, R7_r2, R7_Cant_Dias, R7_pred, R7_Coeficiente
    VariablesParam = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }
    R7_pais = VariablesParam['Variable1']
    R7_Col_Pais = VariablesParam['Variable2']
    R7_Col_Fecha = VariablesParam['Variable3']
    R7_Col_Confirmados = VariablesParam['Variable4']
    R7_Cant_Dias = VariablesParam['Variable5']
    R7_Cant_Dias = float(R7_Cant_Dias)

    Datos = dataset.loc[dataset[R7_Col_Pais]==R7_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R7_Col_Confirmados]

    for i in Datos.index:
        Ejex.append(i)

    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.array(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R7_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R7_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)

    R7_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R7_Coeficiente = modelo.coef_
    R7_r2 = r2_score(Ejey,nueva_y)

    x_nuevo_min = 0.0
    x_nuevo_max = R7_Cant_Dias

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R7_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {} \n Con una prediccion para: {} dias de = {} Infectados'.format(R7_Grado_Polinomio, round(R7_rmse,2), round(R7_r2,2), R7_Cant_Dias,round(R7_pred,2))
    plt.title("Tendencia del número de infectados por día de un País.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte7.png")
    plt.close()
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte8', methods=['GET'])
def getReporte8():
    if R8_Coeficiente[3] >0:
        conclusion = 'Con nuestra prediccion realizada para un año y el modelo generado con un\ncoeficiente que resulta ser positivo, podemos concluir que la prediccion de casos\nen este pais ira aumentando si la pandemia no se logra controlar a tiempo'
    else:
        conclusion = 'Con nuestra prediccion realizada para un año y el modelo generado con un\ncoeficiente que resulta ser negativo, podemos concluir que la prediccion de casos\nen este pais ira disminuyendo probablemente por que la pandemia en el pais fue controlada'
    with open ("Reporte8.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R8_pais,
                    "grado": R8_Grado_Polinomio, 
                    "RMSE":round(R8_rmse,4),
                    "R2": round(R8_r2,4),
                    "Prediccion":round(R8_pred,4),
                    "Conclusion":conclusion})

@app.route('/Reporte8', methods =['POST'])
def Reporte8():
    global R8_pais, R8_col_pais, R8_col_confirmados, R8_Grado_Polinomio, R8_rmse, R8_r2, R8_pred, R8_Coeficiente
    regr = linear_model.LinearRegression()
    VariablesParamR8 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
    }
    R8_pais = VariablesParamR8['Variable1']
    R8_col_pais = VariablesParamR8['Variable2']
    R8_col_confirmados= VariablesParamR8['Variable3']

    Datos = dataset.loc[dataset[R8_col_pais]==R8_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R8_col_confirmados]

    for i in Datos.index:
        Ejex.append(i)
    

    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R8_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R8_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Ejey)

    nueva_y = modelo.predict(Transform_x)
    
    R8_rmse = np.sqrt(mean_squared_error(Ejey,nueva_y))
    R8_Coeficiente = modelo.coef_
    print(R8_Coeficiente)
    R8_r2 = r2_score(Ejey,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = 365

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R8_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {} \n prediccion de casos a un año: {}'.format(R8_Grado_Polinomio, round(R8_rmse,2), round(R8_r2,2), round(R8_pred,2))
    plt.title("Predicción de casos de un país para un año\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte8.png")
    plt.close()


    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte9', methods=['GET'])
def getReporte9():
    if R9_m > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion resultante es mayor a 1, podemos concluir\nque la tendencia de vacunacion en el pais ira creciendo de forma rapida conforme\nal tiempo pase, por lo cual la pandemia sera un riesgo menos para el pais'
    elif R9_m< 1 or R9_m > 0 :
        conclusion = 'Dado a que la pendiente de nuestra ecuacion resultante se encuentra en un valor\nentre 0 y 1, nos indica que la tendencia de vacunacion en el pais seguira creciendo pero\na un nivel mas constante, no tan rapido como si lo fuese mayor a 1, por lo cual\n esto nos indica que la mayoria de las personas no muestran interes en vacunarse'
    elif R9_m < 0:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion resultante es menor a 0, en este caso\nnegativa, podemos concluir que conforme el tiempo avanza las personas no quieren ser\nvacunadas en contra del covid-19'
    with open ("Reporte9.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R9_pais,
                    "formula": R9_Formula, 
                    "RMSE":round(R9_rmse,4),
                    "R2": round(R9_r2,4),
                    "coef": R9_m,
                    "intercept": round(R9_b,2),
                    "Conclusion":conclusion})

@app.route('/Reporte9', methods = ['POST'])
def Reporte9():
    global R9_pais, R9_col_pais, R9_col_vacunacion, R9_col_dias, R9_m, R9_b, R9_r2, R9_rmse, R9_Formula
    regr = linear_model.LinearRegression()
    VariablesParamR9 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }
    R9_pais = VariablesParamR9['Variable1']
    R9_col_pais = VariablesParamR9['Variable2']
    R9_col_vacunacion= VariablesParamR9['Variable3']
    R9_col_dias= VariablesParamR9['Variable4']

    Datos = dataset.loc[dataset[R9_col_pais]==R9_pais]
    Datos = pd.DataFrame(Datos)

    Ejex = Datos[R9_col_dias]

    y = Datos[R9_col_vacunacion]
    X = pd.to_datetime(Ejex).astype(np.int64)
    X = X[:,np.newaxis]
    regr.fit(X,y)
    R9_m = regr.coef_[0]
    R9_b = regr.intercept_
    y_p = regr.predict(X)
    plt.scatter(X,y, color = 'black')
    plt.plot(X,y_p,color = 'blue')
    R9_r2 = r2_score(y,y_p)
    R9_rmse = np.sqrt(mean_squared_error(y, y_p))
    R9_Formula = 'y={0}*x+{1}'.format(R9_m, round(R9_b,2))
    Titulo = 'Ecuación: {}; RMSE = {}; R2 = {}'.format(R9_Formula, round(R9_rmse,2), round(R9_r2,2))
    plt.title("Tendencia de la vacunación de en un País.\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte9.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte10', methods=['GET'])
def getReporte10():
    if R10_coeficiente[3] > R10_coeficiente2[3]:
        conclusion = 'Gracias a los modelos generados para cada pais y los resultados obtenidos\npodemos determinar que el país '+ R10_pais_1 + ' Presenta una mejor tasa o\ncomportamiento de vacunación en sus habitantes'
    elif R10_coeficiente[3] < R10_coeficiente2[3]:
        conclusion = 'Gracias a los modelos generados para cada pais y los resultados obtenidos\npodemos determinar que el país '+ R10_pais_2 + ' Presenta una mejor tasa o\ncomportamiento de vacunación en sus habitantes'
    else:
        conclusion = 'Gracias a los modelos generados para cada pais y los resultados obtenidos\npodemos determinar los paises presentan una tasa de vacunación similar\n en sus habitantes'
        
    with open ("Reporte101.png","rb") as imagen:
        cadenaBase64i1 = base64.b64encode(imagen.read())
    with open ("Reporte102.png","rb") as imagen2:
        cadenaBase64i2 = base64.b64encode(imagen2.read())
    return jsonify({"imagen1":cadenaBase64i1.decode('utf-8'),
                    "imagen2":cadenaBase64i2.decode('utf-8'),
                    "pais1":R10_pais_1,
                    "pais2":R10_pais_2,
                    "grado": R10_Grado_Polinomio, 
                    "RMSE1":round(R10_rmse,4),
                    "R21": round(R10_r2,4),
                    "RMSE2":round(R10_rmse2,4),
                    "R22": round(R10_r22,4),
                    "Conclusion":conclusion})

@app.route('/Reporte10', methods = ['POST'])
def Reporte10():
    global R10_pais_1, R10_pais_2, R10_Col_pais, R10_Col_vacunacion, R10_Col_Fecha, R10_Grado_Polinomio, R10_r2, R10_rmse, R10_rmse2, R10_r22, R10_coeficiente, R10_coeficiente2
    VariablesParamR10 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R10_pais_1 = VariablesParamR10['Variable1']
    R10_pais_2 = VariablesParamR10['Variable2']
    R10_Col_pais= VariablesParamR10['Variable3']
    R10_Col_vacunacion = VariablesParamR10['Variable4']
    R10_Col_Fecha = VariablesParamR10['Variable5']

    Datos = dataset.loc[dataset[R10_Col_pais]==R10_pais_1]
    Datos = pd.DataFrame(Datos)
    Datos2 = dataset.loc[dataset[R10_Col_pais]==R10_pais_2]
    Datos2 = pd.DataFrame(Datos2)
    Ejex = Datos[R10_Col_Fecha]
    Ejey = Datos[R10_Col_vacunacion]

    Ejex2 = Datos2[R10_Col_Fecha]
    Ejey2 = Datos2[R10_Col_vacunacion]

    X = pd.to_datetime(Ejex).astype(np.int64)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R10_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R10_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R10_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R10_coeficiente = modelo.coef_[0]
    R10_r2 = r2_score(Y,nueva_y)
    plt.plot(Ejex, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R10_pais_1, R10_Grado_Polinomio, round(R10_rmse,2), round(R10_r2,2))
    plt.title("Ánalisis Comparativo de Vacunación entre 2 paises.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte101.png")
    plt.close()

    X2 = pd.to_datetime(Ejex2).astype(np.int64)
    X2 = X2[:,np.newaxis]
    Y2 = Ejey2[:,np.newaxis]
    plt.scatter(Ejex2,Y2)

    R10_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R10_Grado_Polinomio)
    Transform_x2 = Caracteristicas_Polinomio.fit_transform(X2)
    modelo2 = linear_model.LinearRegression().fit(Transform_x2,Y2)

    nueva_y2 = modelo2.predict(Transform_x2)

    R10_rmse2 = np.sqrt(mean_squared_error(Y2,nueva_y2))
    R10_coeficiente2 = modelo.coef_[0]
    R10_r22 = r2_score(Y2,nueva_y2)

    plt.plot(Ejex2, Y2, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R10_pais_2, R10_Grado_Polinomio, round(R10_rmse2,2), round(R10_r22,2))
    plt.title("Ánalisis Comparativo de Vacunación entre 2 paises.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte102.png")
    plt.close()


    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte11', methods=['GET'])
def getReporte11():
    if R11_m[0] > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion mayor a 1, podemos concluir\nque el porcentaje de hombres infectados crecera demasiado rapido conforme al tiempo\npase, por lo cual la pandemia sera un riesgo para la poblacion'
    elif R11_m[0]< 1 or R11_m[0] > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos indica\nque el porcentaje seguira creciendo pero a un nivel mas constante, no tan rapido\ncomo si lo fuese mayor a 1, por lo cual puede ser posible que la pandemia se haya\ncontrolado un poco'
    elif R11_m[0] < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos\nconcluir que conforme el tiempo transcurra la pandemia ira disminuyendo hasta que ya\nno exista más, por lo cual ya no se tendrán hombres infectados'
    with open ("Reporte11.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R11_pais,
                    "formula": R11_Formula, 
                    "RMSE":round(R11_rmse,4),
                    "R2": round(R11_r2,4),
                    "coef": R11_m[0],
                    "intercept": round(R11_b[0],2),
                    "Conclusion": conclusion})

@app.route('/Reporte11', methods = ['POST'])
def Reporte11():
    global R11_pais, R11_col_pais,R11_Genero, R11_col_infectados, R11_col_genero, R11_col_fecha, R11_Formula, R11_r2, R11_rmse, R11_m, R11_b
    VariablesParamR11 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
        "Variable6":request.json['Variable6']
    }
    regr = linear_model.LinearRegression()
    R11_pais = VariablesParamR11['Variable1']
    R11_col_pais = VariablesParamR11['Variable2']
    R11_col_infectados = VariablesParamR11['Variable3']
    R11_col_genero = VariablesParamR11['Variable4']
    R11_Genero = VariablesParamR11['Variable5']
    R11_col_fecha = VariablesParamR11['Variable6']


    Datos = dataset.loc[dataset[R11_col_pais]==R11_pais]
    Datos = pd.DataFrame(Datos)

    var1 = Datos[R11_col_genero]

    Datos2 = Datos.loc[Datos[R11_col_genero]==R11_Genero]
    Datos2 = pd.DataFrame(Datos2)

    Ejex = Datos2[R11_col_genero]
    Ejey = Datos2[R11_col_infectados]
    Fechas = Datos2[R11_col_fecha]

    var2 = []
    #Prueba = (Ejex *100)/Ejey
    for i in Ejex.index:
        var2.append(i)

    resultado = []

    for i in range(len(var2)):
        resultado = var2[i]/var1.size
    print(resultado)
    '''
    Y = Prueba[:,np.newaxis]

    Eje_Xf = pd.to_datetime(Fechas).astype(np.int64)
    Eje_Xf = Eje_Xf[:,np.newaxis]

    for i in range(len(Y)):
        if np.isnan(Y[i]):
            Y[i] = 0.0
 
    regr.fit(Eje_Xf,Y)
    R11_coef = regr.coef_
    R11_m = regr.coef_[0]
    R11_b = regr.intercept_
    R11_y_p = regr.predict(Eje_Xf)

    print(R11_m[0])
    print(R11_b[0])

    plt.scatter(Eje_Xf,Y,color = 'black')
    plt.plot(Eje_Xf,R11_y_p, color = 'blue')
    R11_Formula = 'y={0}*x+{1}'.format(R11_m[0], R11_b[0])
    R11_r2 = r2_score(Y,R11_y_p)
    R11_rmse = np.sqrt(mean_squared_error(Y,R11_y_p))

    Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R11_Formula, R11_coef, round(R11_rmse,4), round(R11_r2,4))
    plt.title("Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo.\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte11.png")
    plt.close()
    '''
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte13', methods=['GET'])
def getReporte13():
    if R13_coeficiente[3] > R13_coeficiente2[3]:
        conclusion = 'Gracias a los modelos generados para casos confirmados vs muerte y edad vs\nmuerte y los resultados obtenidos podemos determinar que los casos confirmados vs\nmuertes son mayores a la edad vs muerte'
    elif R13_coeficiente[3] < R13_coeficiente2[3]:
        conclusion = 'Gracias a los modelos generados para casos confirmados vs muerte y edad vs\nmuerte y los resultados obtenidos podemos determinar que la edad vs muertes son\nmayores a los casos confirmados vs muerte'
    else:
        conclusion = 'Gracias a los modelos generados para casos confirmados vs muerte y edad vs\nmuerte y los resultados obtenidos podemos determinar que el pais presenta una\nrelacion similar entre la edad y los casos confirmados'
    with open ("Reporte131.png","rb") as imagen:
        cadenaBase64i1 = base64.b64encode(imagen.read())
    with open ("Reporte132.png","rb") as imagen2:
        cadenaBase64i2 = base64.b64encode(imagen2.read())
    return jsonify({"imagen1":cadenaBase64i1.decode('utf-8'),
                    "imagen2":cadenaBase64i2.decode('utf-8'),
                    "pais1":R13_pais,
                    "grado": R13_Grado_Polinomio, 
                    "RMSE1":round(R13_rmse,4),
                    "R21": round(R13_r2,4),
                    "RMSE2":round(R13_rmse2,4),
                    "R22": round(R13_r22,4),
                    "Conclusion":conclusion})

@app.route('/Reporte13',methods = ['POST'])
def Reporte13():
    global R13_pais, R13_col_pais, R13_col_infectados, R13_col_muertes, R13_col_edad, R13_rmse, R13_r2, R13_rmse2, R13_r22, R13_Grado_Polinomio, R13_coeficiente, R13_coeficiente2
    VariablesParamR13 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5']
    }

    R13_pais = VariablesParamR13['Variable1']
    R13_col_pais = VariablesParamR13['Variable2']
    R13_col_infectados = VariablesParamR13['Variable3']
    R13_col_muertes = VariablesParamR13['Variable4']
    R13_col_edad = VariablesParamR13['Variable5']

    Datos = dataset.loc[dataset[R13_col_pais]==R13_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = Datos[R13_col_infectados]
    Ejey = Datos[R13_col_muertes]

    Ejex2 = Datos[R13_col_muertes]
    Ejey2 = Datos[R13_col_edad]


    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = Ejex[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R13_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R13_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R13_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R13_coeficiente = modelo.coef_[0]
    R13_r2 = r2_score(Y,nueva_y)

    plt.plot(Ejex, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R13_pais, R13_Grado_Polinomio, round(R13_rmse,2), round(R13_r2,2))
    plt.title("Muertes promedio por casos confirmados y edad de covid 19 en un País.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte131.png")
    plt.close()

    #X2 = pd.to_datetime(Ejex2).astype(np.int64)
    X2 = Ejex2[:,np.newaxis]
    Y2 = Ejey2[:,np.newaxis]
    plt.scatter(Ejex2,Y2)

    R13_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R13_Grado_Polinomio)
    Transform_x2 = Caracteristicas_Polinomio.fit_transform(X2)
    modelo2 = linear_model.LinearRegression().fit(Transform_x2,Y2)

    nueva_y2 = modelo2.predict(Transform_x2)

    R13_rmse2 = np.sqrt(mean_squared_error(Y2,nueva_y2))
    R13_coeficiente2 = modelo.coef_[0]
    R13_r22 = r2_score(Y2,nueva_y2)

    plt.plot(X2, Y2, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R13_pais, R13_Grado_Polinomio, round(R13_rmse2,2), round(R13_r22,2))
    plt.title("Muertes promedio por casos confirmados y edad de covid 19 en un País.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte132.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte14', methods=['GET'])
def getReporte14():
    if R14_Coeficiente[3] >0:
        conclusion = 'Con nuestra prediccion realizada para un año y el modelo generado con un\ncoeficiente que resulta ser positivo, podemos concluir que las muertes de personas\npara estas regiones ira aumentando si la pandemia no se logra controlar a tiempo'
    else:
        conclusion = 'Con nuestra prediccion realizada para un año y el modelo generado con un\ncoeficiente que resulta ser negativo, podemos concluir que las muertes para estas\nregiones iran disminuyendo, con el paso del tiempo'
    with open ("Reporte14.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())    
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R14_pais,
                    "grado": R14_Grado_Polinomio, 
                    "RMSE":round(R14_rmse,4),
                    "R2": round(R14_r2,4),
                    "Conclusion":conclusion})

@app.route('/Reporte14', methods = ['POST'])
def Reporte14():
    global R14_pais, R14_col_pais, R14_col_region, R14_col_muertes, R14_Grado_Polinomio, R14_rmse, R14_r2, R14_Coeficiente
    VariablesParamR14 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }

    R14_pais = VariablesParamR14['Variable1']
    R14_col_pais = VariablesParamR14['Variable2']
    R14_col_region = VariablesParamR14['Variable3']
    R14_col_muertes = VariablesParamR14['Variable4']

    Datos = dataset.loc[dataset[R14_col_pais]==R14_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = Datos[R14_col_region]
    Eje_x = []
    Ejey = Datos[R14_col_muertes]

    Ejex = np.asarray(Ejex)
    for i in Datos.index:
        Eje_x.append(i)
    
    X = np.asarray(Eje_x)

    plt.xticks(X, Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]

    
    R14_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R14_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R14_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R14_Coeficiente = modelo.coef_[0]
    print(R14_Coeficiente)
    R14_r2 = r2_score(Y,nueva_y)

    plt.plot(X, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R14_pais, R14_Grado_Polinomio, round(R14_rmse,2), round(R14_r2,2))
    plt.title("Muertes según regiones de un país - Covid 19.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte14.png")
    plt.close()
    
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte15', methods=['GET'])
def getReporte15():
    if R15_Coeficiente[3] >0:
        conclusion = 'Con el modelo generado y sus resultados se puede concluir que la tendencia\nde los casos confirmados en este departamento, seguirá en aumento mientras que la\npandemia no sea controlada'
    else:
        conclusion = 'Con el modelo generado y sus resultados se puede concluir que la tendencia\nde los casos confirmados en este departamento, seguirá en disminucion ya que la\npandemia ha sido controlada'
    with open ("Reporte15.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())    
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R15_pais,
                    "grado": R15_Grado_Polinomio, 
                    "RMSE":round(R15_rmse,4),
                    "R2": round(R15_r2,4),
                    "Conclusion":conclusion})

@app.route('/Reporte15', methods = ['POST'])
def Reporte15():
    global R15_pais, R15_Departamento, R15_col_pais, R15_col_departamento, R15_col_fecha, R15_col_infectados, R15_Grado_Polinomio, R15_rmse, R15_r2, R15_Coeficiente
    VariablesParamR15 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
        "Variable6":request.json['Variable6']
    }

    R15_pais = VariablesParamR15['Variable1']
    R15_col_pais = VariablesParamR15['Variable2']
    R15_Departamento = VariablesParamR15['Variable3']
    R15_col_departamento = VariablesParamR15['Variable4']
    R15_col_fecha = VariablesParamR15['Variable5']
    R15_col_infectados = VariablesParamR15['Variable6']

    Datos = dataset.loc[dataset[R15_col_pais]==R15_pais]
    Datos = pd.DataFrame(Datos)

    Datos2 = Datos.loc[Datos[R15_col_departamento]==R15_Departamento]
    Datos2 = pd.DataFrame(Datos2)

    Ejex = Datos2[R15_col_fecha]
    Ejey = Datos2[R15_col_infectados]

    X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = np.asarray(Ejey)[:,np.newaxis]

    plt.scatter(X,Y)

    R15_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R15_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R15_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R15_Coeficiente = modelo.coef_[0]
    R15_r2 = r2_score(Y,nueva_y)

    plt.plot(X, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Departamento: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R15_pais,R15_Departamento, R15_Grado_Polinomio, round(R15_rmse,2), round(R15_r2,2))
    plt.title("Tendencia de casos confirmados de Coronavirus en un departamento de un País.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte15.png")
    plt.close()
 
    
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte16', methods=['GET'])
def getReporte16():
    if R16_m[0] > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion mayor a 1, podemos concluir\nque porcentaje de muertes frente a los casos confirmados ira en aumento conforme\nel tiempo avance'
    elif R16_m[0]< 1 or R16_m[0] > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos indica\nque el porcentaje de muertes tendra un aumento constante un poco menor a si la\npendiente fuese mayor a 1'
    elif R16_m[0] < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos\nconcluir que conforme el tiempo transcurra el porcentaje de muertes ira en disminución'
    with open ("Reporte16.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R16_pais,
                    "formula": R16_Formula, 
                    "RMSE":round(R16_rmse,4),
                    "R2": round(R16_r2,4),
                    "coef": R16_m[0],
                    "intercept": R16_b[0],
                    "Conclusion":conclusion})

@app.route('/Reporte16', methods = ['POST'])
def Reporte16():
    global R16_pais,R16_col_pais,R16_Region,R16_col_region,R16_continente, R16_col_continente, R16_col_muertes, R16_col_casos, R16_Formula, R16_r2, R16_rmse, R16_m, R16_b
    regr = linear_model.LinearRegression()
    VariablesParamR16 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
        "Variable6":request.json['Variable6'],
        "Variable7":request.json['Variable7'],
        "Variable8":request.json['Variable8']

    }

    R16_pais = VariablesParamR16['Variable1']
    R16_col_pais = VariablesParamR16['Variable2']
    R16_Region = VariablesParamR16['Variable3']
    R16_col_region = VariablesParamR16['Variable4']
    R16_continente = VariablesParamR16['Variable5']
    R16_col_continente = VariablesParamR16['Variable6']
    R16_col_muertes = VariablesParamR16['Variable7']
    R16_col_casos = VariablesParamR16['Variable8']

    if R16_pais != '':
        Datos = dataset.loc[dataset[R16_col_pais]==R16_pais]
        Datos = pd.DataFrame(Datos)
        Ejex = Datos[R16_col_muertes]
        Ejey = Datos[R16_col_casos]
        
        Prueba = (Ejex *100)/Ejey
        Y = Prueba[:,np.newaxis]

        for i in range(len(Y)):
            if np.isnan(Y[i]):
                Y[i] = 0.0
        Ejey = Ejey[:,np.newaxis]
        
        regr.fit(Ejey,Y)
        R16_coef = regr.coef_
        R16_m = regr.coef_[0]
        R16_b = regr.intercept_
        R16_y_p = regr.predict(Ejey)
        plt.scatter(Ejey,Y,color = 'black')
        plt.plot(Ejey,R16_y_p, color = 'blue')
        R16_Formula = 'y={0}*x+{1}'.format(R16_m[0], R16_b[0])
        R16_r2 = r2_score(Y,R16_y_p)
        R16_rmse = np.sqrt(mean_squared_error(Y,R16_y_p))

        Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R16_Formula, R16_coef,2, round(R16_rmse,2), round(R16_r2,2))
        plt.title("Porcentaje de muertes frente al total de casos en un país, región o continente.\n " + Titulo, fontsize=10)
        plt.xlabel('Casos')
        plt.ylabel('Porcentaje Muertes')
        plt.savefig("Reporte16.png")
        plt.close()
        
    elif R16_continente != '':
        Datos = dataset.loc[dataset[R16_col_continente]==R16_continente]
        Datos = pd.DataFrame(Datos)
        Ejex = Datos[R16_col_muertes]
        Ejey = Datos[R16_col_casos]
        
        Prueba = (Ejex *100)/Ejey
        Y = Prueba[:,np.newaxis]

        for i in range(len(Y)):
            if np.isnan(Y[i]):
                Y[i] = 0.0
            
        print(Y)
        Ejey = Ejey[:,np.newaxis]
        
        regr.fit(Ejey,Y)
        R16_coef = regr.coef_
        R16_m = regr.coef_[0]
        R16_b = regr.intercept_
        R16_y_p = regr.predict(Ejey)
        plt.scatter(Ejey,Y,color = 'black')
        plt.plot(Ejey,R16_y_p, color = 'blue')
        R16_Formula = 'y={0}*x+{1}'.format(R16_m[0], R16_b[0])
        R16_r2 = r2_score(Y,R16_y_p)
        R16_rmse = np.sqrt(mean_squared_error(Y,R16_y_p))

        Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R16_Formula, R16_coef,2, round(R16_rmse,2), round(R16_r2,2))
        plt.title("Porcentaje de muertes frente al total de casos en un país, región o continente.\n " + Titulo, fontsize=10)
        plt.xlabel('Casos')
        plt.ylabel('Porcentaje Muertes')
        plt.savefig("Reporte16.png")
        plt.close()
    elif R16_Region != '':
        Datos = dataset.loc[dataset[R16_col_region]==R16_Region]
        Datos = pd.DataFrame(Datos)
        Ejex = Datos[R16_col_muertes]
        Ejey = Datos[R16_col_casos]
        
        Prueba = (Ejex *100)/Ejey
        Y = Prueba[:,np.newaxis]

        for i in range(len(Y)):
            if np.isnan(Y[i]):
                Y[i] = 0.0
            
        print(Y)
        Ejey = Ejey[:,np.newaxis]
        
        regr.fit(Ejey,Y)
        R16_coef = regr.coef_
        R16_m = regr.coef_[0]
        R16_b = regr.intercept_
        R16_y_p = regr.predict(Ejey)
        plt.scatter(Ejey,Y,color = 'black')
        plt.plot(Ejey,R16_y_p, color = 'blue')
        R16_Formula = 'y={0}*x+{1}'.format(R16_m[0], R16_b[0])
        R16_r2 = r2_score(Y,R16_y_p)
        R16_rmse = np.sqrt(mean_squared_error(Y,R16_y_p))

        Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R16_Formula, R16_coef,2, round(R16_rmse,2), round(R16_r2,2))
        plt.title("Porcentaje de muertes frente al total de casos en un país, región o continente.\n " + Titulo, fontsize=10)
        plt.xlabel('Casos')
        plt.ylabel('Porcentaje Muertes')
        plt.savefig("Reporte16.png")
        plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte17', methods=['GET'])
def getReporte17():
    if R17_m[0] > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion mayor a 1, podemos concluir\nque la tasa de comportamiento de los casos activos en relacion al numero de muertes\ndel continente va en aumento'
    elif R17_m[0]< 1 or R17_m[0] > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos indica\nque la tasa de comportamiento de los casos activos en relacion al numero de muertes\ndel continente aumenta de manera constante'
    elif R17_m[0] < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos\nconcluir que conforme el tiempo transcurra la tasa de comportamiento de los casos\nactivos en relacion al numero de muertes del continente disminuye de manera constante'
    with open ("Reporte17.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R17_Continente,
                    "formula": R17_Formula, 
                    "RMSE":round(R17_rmse,4),
                    "R2": round(R17_r2,4),
                    "coef": R17_m[0],
                    "intercept": R17_b[0],
                    "Conclusion":conclusion})

@app.route('/Reporte17', methods = ['POST'])
def Reporte17():
    global R17_Continente, R17_col_continente, R17_col_muertes, R17_col_casos, R17_Formula, R17_rmse, R17_r2, R17_m, R17_b
    regr = linear_model.LinearRegression()
    VariablesParamR17 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']

    }

    R17_Continente = VariablesParamR17['Variable1']
    R17_col_continente = VariablesParamR17['Variable2']
    R17_col_muertes = VariablesParamR17['Variable3']
    R17_col_casos = VariablesParamR17['Variable4']

    Datos = dataset.loc[dataset[R17_col_continente]==R17_Continente]
    Datos = pd.DataFrame(Datos)
    Ejex = Datos[R17_col_casos]
    Ejey = Datos[R17_col_muertes]
    
    Ejex = Ejex[:,np.newaxis]
    Ejey = Ejey[:,np.newaxis]
    
    regr.fit(Ejex,Ejey)
    R17_coef = regr.coef_
    R17_m = regr.coef_[0]
    R17_b = regr.intercept_
    R17_y_p = regr.predict(Ejex)
    plt.scatter(Ejex,Ejey,color = 'black')
    plt.plot(Ejex,R17_y_p, color = 'blue')
    R17_Formula = 'y={0}*x+{1}'.format(R17_m[0], R17_b[0])
    R17_r2 = r2_score(Ejey,R17_y_p)
    R17_rmse = np.sqrt(mean_squared_error(Ejey,R17_y_p))

    Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R17_Formula, R17_coef,2, round(R17_rmse,2), round(R17_r2,2))
    plt.title("Tasa de comportamiento de casos activos en relación al número de muertes en un continente.\n " + Titulo, fontsize=10)
    plt.xlabel('Casos')
    plt.ylabel('Muertes')
    plt.savefig("Reporte17.png")
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/Reporte18', methods =['POST'])
def Reporte18():

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte19', methods=['GET'])
def getReporte19():
    if R19_Coeficiente[3] >0:
        conclusion = 'Con el modelo generado y sus resultados se puede concluir que el numero\nde muertes del ultimo día del año aun iran en aumento debido al mal control de la\npandemia Covid 19'
    else:
        conclusion = 'Con el modelo generado y sus resultados se puede concluir que el numero\nde muertes del ultimo dia del año presentarán una disminución'
    with open ("Reporte19.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())    
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R19_pais,
                    "grado": R19_Grado_Polinomio, 
                    "RMSE":round(R19_rmse,4),
                    "R2": round(R19_r2,4),
                    "Conclusion":conclusion})

@app.route('/Reporte19', methods =['POST'])
def Reporte19():

    global R19_pais, R19_col_pais, R19_col_Dias, R19_col_muertes, R19_Grado_Polinomio, R19_rmse, R19_r2, R19_Coeficiente
    VariablesParamR19 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }

    R19_pais = VariablesParamR19['Variable1']
    R19_col_pais = VariablesParamR19['Variable2']
    R19_col_muertes = VariablesParamR19['Variable3']
    R19_col_Dias = VariablesParamR19['Variable4']   

    Datos = dataset.loc[dataset[R19_col_pais]==R19_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = []
    Ejey = Datos[R19_col_muertes]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(Ejex,Y)

    R19_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R19_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)
    
    R19_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R19_Coeficiente = modelo.coef_[0]
    R19_r2 = r2_score(Y,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = 365.0

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R19_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}; \n Con una prediccion para: {} dias de = {} muertes'.format(R19_Grado_Polinomio, R19_rmse, R19_r2, 365,R19_pred)
    plt.title("Predicción de muertes en el último día del primer año de infecciones en un país.\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte19.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte20', methods = ['GET'])
def getReporte20():
    if tasa1 > tasa2:
        conclusion = 'podemos concluir que la tasa de casos diarios vs casos acumulados, es\nmayor a la tasa de muertes vs casos acumulados '
    elif tasa2 > tasa1:
        conclusion = 'podemos concluir que la tasa de tasa de muertes vs casos acumulados, es\nmayor a la de casos diarios vs casos acumulados '
    else:
        conclusion = 'podemos concluir que la tasa de casos diarios vs casos acumulados es\nsimilar a la tasa de muertes vs casos acumulados '
    with open ("Reporte20.png","rb") as imagen:
        cadenaBase64i1 = base64.b64encode(imagen.read())
    with open ("Reporte201.png","rb") as imagen2:
        cadenaBase64i2 = base64.b64encode(imagen2.read())
    return jsonify({"imagen1":cadenaBase64i1.decode('utf-8'),
                    "imagen2":cadenaBase64i2.decode('utf-8'),
                    "t1":tasa1,
                    "t2":tasa2,
                    "Conclusion":conclusion})

@app.route('/Reporte20', methods = ['POST'])
def Reporte20():
    global R20_col_casos, R20_col_diarios, R20_col_muertes, tasa1, tasa2
    regr = linear_model.LinearRegression()
    VariablesParamR20 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3']

    }
    R20_col_casos = VariablesParamR20['Variable1']
    R20_col_diarios = VariablesParamR20['Variable2']
    R20_col_muertes = VariablesParamR20['Variable3']

    Datos = pd.DataFrame(dataset)
    Ejex = Datos[R20_col_casos]
    Ejey = Datos[R20_col_diarios]

    Resultado = Ejey / Ejex * 100

    tasa1 = str(round(Resultado.mean(),2))

    AuxX = Datos[R20_col_casos]

    plt.plot(AuxX, Resultado)
    plt.title("Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios\n ", fontsize=10)
    plt.xlabel('Casos')
    plt.ylabel('Casos diarios')
    plt.savefig("Reporte20.png")
    plt.close()

    Datos = pd.DataFrame(dataset)
    Ejex = Datos[R20_col_casos]
    Ejey = Datos[R20_col_muertes]

    Resultado = Ejey / Ejex * 100
    tasa2 = str(round(Resultado.mean(),2))

    AuxX = Datos[R20_col_casos]

    plt.plot(AuxX, Resultado)
    plt.title("Tasa de crecimiento de casos de COVID-19 en relación con las muertes\n ", fontsize=10)
    plt.xlabel('Casos')
    plt.ylabel('Muertes')
    plt.savefig("Reporte201.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte21', methods=['GET'])
def getReporte21():
    if R21_pred[0] < R21_pred2[0]:
        conclusion= 'Para la prediccion realizada con los modelos obtenidoss podemos determinar\nque las muertes son menores a los casos en todo el mundo'
    elif R21_pred[0] > R21_pred2[0]:
        conclusion= 'Para la prediccion realizada con los modelos obtenidoss podemos determinar\nque los casos son menores a las muertes en todo el mundo'
    else:
        conclusion='Para la prediccion realizada con los modelos obtenidoss podemos determinar\nque los casos son iguales a las muertes en todo el mundo'
    with open ("Reporte21.png","rb") as imagen:
        cadenaBase64i1 = base64.b64encode(imagen.read())
    with open ("Reporte212.png","rb") as imagen2:
        cadenaBase64i2 = base64.b64encode(imagen2.read())
    return jsonify({"imagen1":cadenaBase64i1.decode('utf-8'),
                    "imagen2":cadenaBase64i2.decode('utf-8'),
                    "grado": R21_Grado_Polinomio, 
                    "RMSE1":round(R21_rmse,4),
                    "R21": round(R21_r2,4),
                    "RMSE2":round(R21_rmse2,4),
                    "R22": round(R21_r22,4),
                    "pred1":R21_pred[0],
                    "pred2":R21_pred2[0],
                    "Conclusion":conclusion})
                    
@app.route('/Reporte21', methods = ['POST'])
def Reporte21():
    global R21_col_casos, R21_col_muertes, R21_col_fecha, R21_dias, R21_Grado_Polinomio, R21_rmse, R21_r2, R21_pred, R21_rmse2,R21_r22,R21_pred2, R21_Coeficiente2, R21_Coeficiente
    VariablesParamR19 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }

    R21_col_casos = VariablesParamR19['Variable1']
    R21_col_muertes = VariablesParamR19['Variable2']
    R21_col_fecha = VariablesParamR19['Variable3']
    R21_dias = VariablesParamR19['Variable4']
    R21_dias = float(R21_dias)

    Datos = pd.DataFrame(dataset)

    Ejex = []
    Ejey = Datos[R21_col_muertes]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)

    R21_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R21_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)
    
    R21_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R21_Coeficiente = modelo.coef_[0]
    R21_r2 = r2_score(Y,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R21_dias

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R21_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}; \n Con una prediccion para: {} dias de = {} muertes'.format(R21_Grado_Polinomio, R21_rmse, R21_r2, R21_dias,R21_pred)
    plt.title("Predicciones de casos y muertes en todo el mundo.\n " + Titulo, fontsize=10)
    plt.xlabel('Dias')
    plt.ylabel('Muertes')
    plt.savefig("Reporte21.png")
    plt.close()

    Ejex = []
    Ejey = Datos[R21_col_casos]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)

    R21_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R21_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)
    
    R21_rmse2 = np.sqrt(mean_squared_error(Y,nueva_y))
    R21_Coeficiente2 = modelo.coef_[0]
    R21_r22 = r2_score(Y,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R21_dias

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R21_pred2 = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; R2 = {}; \n Con una prediccion para: {} dias de = {} Casos'.format(R21_Grado_Polinomio, R21_rmse2, R21_r22, R21_dias,R21_pred2)
    plt.title("Predicciones de casos y muertes en todo el mundo.\n " + Titulo, fontsize=10)
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.savefig("Reporte212.png")
    plt.close()


    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte_22', methods=['GET'])
def getReporte22():
    if R22_m[0] > 1:
        conclusion = 'Dado a que la pendiente de nuestra ecuacion mayor a 1, podemos concluir que\nla tasa de mortalidad debido a la infeccion ira creciendo de manera muy rapida, lo\ncual es un riesgo para la población mundial'
    elif R22_m[0]< 1 or R22_m[0] > 0 :
        conclusion = 'Dado a que la pendiente se encuentra en un valor entre 0 y 1, nos muestra\nque la tasa de mortalidad debido a la infeccion aumenta lentamente'
    elif R22_m[0] < 0:
        conclusion = 'Dado a que la pendiente es menor a 0, en este caso negativa, podemos\nconcluir que conforme el tiempo transcurra la tasa de mortalidad disminuira'
    with open ("Reporte22.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R22_pais,
                    "formula": R22_Formula, 
                    "RMSE":round(R22_rmse,4),
                    "R2": round(R22_r2,4),
                    "coef": round(R22_m[0],2),
                    "intercept": round(R22_b[0],2),
                    "Conclusion":conclusion})

@app.route('/Reporte22',methods = ['POST'])
def Reporte22():
    global R22_col_muertes, R22_col_infectados, R22_col_pais, R22_pais, R22_col_fecha, R22_Formula, R22_r2, R22_rmse, R22_b, R22_m
    regr = linear_model.LinearRegression()
    VariablesParamR19 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5'],
    }

    R22_pais = VariablesParamR19['Variable1']
    R22_col_pais = VariablesParamR19['Variable2']
    R22_col_muertes = VariablesParamR19['Variable3']
    R22_col_infectados = VariablesParamR19['Variable4']
    R22_col_fecha = VariablesParamR19['Variable5']

    Datos = dataset.loc[dataset[R22_col_pais]==R22_pais]
    Datos = pd.DataFrame(Datos)

    Ejex = []
    Ejey = Datos[R22_col_muertes]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)
 
    regr.fit(X,Y)
    R22_coef = regr.coef_
    R22_m = regr.coef_[0]
    R22_b = regr.intercept_
    R22_y_p = regr.predict(X)
    plt.scatter(X,Y,color = 'black')
    plt.plot(X,R22_y_p, color = 'blue')
    R22_Formula = 'y={0}*x+{1}'.format(R22_m[0], R22_b[0])
    R22_r2 = r2_score(Y,R22_y_p)
    R22_rmse = np.sqrt(mean_squared_error(Y,R22_y_p))

    Titulo = 'Formula : {}; \n coeficiente: {} RMSE = {}; R2 = {}'.format(R22_Formula, R22_coef, round(R22_rmse,2), round(R22_r2,2))
    plt.title("Tasa de mortalidad por coronavirus (COVID-19) en un país.\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte22.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte23', methods=['GET'])
def getReporte23():
    if R23_Coeficiente[3] >0:
        conclusion = 'Se puede concluir que los factores de muerte son un tema a tratar cuando\nse trata de la infeccion por covid 19, ya que se muestra que estos factores aumentan\nla probabilidad de muerte'
    else:
        conclusion = 'se concluye que los factores indicados no tienen relacion con las muertes\npor covid 19'
    with open ("Reporte23.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())    
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "pais":R23_pais,
                    "grado": R23_Grado_Polinomio, 
                    "RMSE":round(R23_rmse,4),
                    "R2": round(R23_r2,4),
                    "Conclusion":conclusion})

@app.route('/Reporte23',methods = ['POST'])
def Reporte23():
    global R23_pais, R23_col_pais, R23_col_muertes, R23_col_factores, R23_Grado_Polinomio, R23_rmse, R23_r2, R23_Coeficiente
    VariablesParamR23 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4']
    }

    R23_pais = VariablesParamR23['Variable1']
    R23_col_pais = VariablesParamR23['Variable2']
    R23_col_muertes = VariablesParamR23['Variable3']
    R23_col_factores = VariablesParamR23['Variable4']

    Datos = dataset.loc[dataset[R23_col_pais]==R23_pais]
    Datos = pd.DataFrame(Datos)
    Ejex = Datos[R23_col_factores]
    Eje_x = []
    Ejey = Datos[R23_col_muertes]

    Ejex = np.asarray(Ejex)
    for i in Datos.index:
        Eje_x.append(i)
    
    X = np.asarray(Eje_x)

    plt.xticks(X, Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]

    
    R23_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R23_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R23_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R23_Coeficiente = modelo.coef_[0]
    print(R23_Coeficiente)
    R23_r2 = r2_score(Y,nueva_y)

    plt.plot(X, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R23_pais, R23_Grado_Polinomio, round(R23_rmse,2), round(R23_r2,2))
    plt.title("Factores de muerte por COVID-19 en un país.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte23.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte24', methods=['GET'])
def getReporte24():
    if R24_Coeficiente[3] > R24_Coeficiente2[3]:
        conclusion = 'Se logra determinar que el numero de casos detectados es mayor al numeró\nde pruebas realizadas en el país'
    elif R24_Coeficiente[3] < R24_Coeficiente2[3]:
        conclusion = 'Se logra determinar que el numero de pruebas es mayor al numeró de casos\ndetectados en el país'
    else:
        conclusion = 'se determina que el numero de pruebas realizadas es igual al numero de\ncasos detectados en el país, dando un indice de positividad del 100%'
    with open ("Reporte24.png","rb") as imagen:
        cadenaBase64i1 = base64.b64encode(imagen.read())
    with open ("Reporte242.png","rb") as imagen2:
        cadenaBase64i2 = base64.b64encode(imagen2.read())
    return jsonify({"imagen1":cadenaBase64i1.decode('utf-8'),
                    "imagen2":cadenaBase64i2.decode('utf-8'),
                    "pais":R24_pais,
                    "grado": R24_Grado_Polinomio, 
                    "RMSE1":round(R24_rmse,4),
                    "R21": round(R24_r2,4),
                    "RMSE2":round(R24_rmse2,4),
                    "R22": round(R24_r22,4),
                    "Conclusion":conclusion})

@app.route('/Reporte24', methods = ['POST'])
def Reporte24():
    global R24_pais, R24_col_pais, R24_col_casos, R24_col_cantpruebas, R24_col_fecha, R24_Grado_Polinomio, R24_rmse, R24_r2, R24_rmse2, R24_r22, R24_Coeficiente, R24_Coeficiente2
    VariablesParamR23 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3'],
        "Variable4":request.json['Variable4'],
        "Variable5":request.json['Variable5']
    }

    R24_pais = VariablesParamR23['Variable1']
    R24_col_pais = VariablesParamR23['Variable2']
    R24_col_casos = VariablesParamR23['Variable3']
    R24_col_cantpruebas = VariablesParamR23['Variable4']
    R24_col_fecha = VariablesParamR23['Variable5']

    Datos = dataset.loc[dataset[R24_col_pais]==R24_pais]
    Datos = pd.DataFrame(Datos)

    Ejex = []
    Ejey = Datos[R24_col_casos]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)

    R24_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R24_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R24_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R24_Coeficiente = modelo.coef_[0]
    R24_r2 = r2_score(Y,nueva_y)

    plt.plot(X, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R24_pais, R24_Grado_Polinomio, round(R24_rmse,2), round(R24_r2,2))
    plt.title("Comparación entre el número de casos detectados y el número de pruebas de un país.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte24.png")
    plt.close()

    Ejex = []
    Ejey = Datos[R24_col_cantpruebas]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)

    R24_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R24_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)

    R24_rmse2 = np.sqrt(mean_squared_error(Y,nueva_y))
    R24_Coeficiente2 = modelo.coef_[0]
    R24_r22 = r2_score(Y,nueva_y)

    plt.plot(X, Y, color='coral', linewidth=3)
    plt.grid()
    Titulo = 'Pais: {} \n Grado = {}; RMSE = {}; R2 = {}'.format(R24_pais, R24_Grado_Polinomio, round(R24_rmse2,2), round(R24_r22,2))
    plt.title("Comparación entre el número de casos detectados y el número de pruebas de un país.\n " + Titulo, fontsize=10)
    plt.savefig("Reporte242.png")
    plt.close()

    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

@app.route('/GetReporte25', methods=['GET'])
def getReporte25():
    if R25_coeficiente[3] > 0:
        Conclusion = 'Debido a que la grafica muestra una pendiente positiva, en el futuro aun\ntendremos aumento de casos confirmados para la infeccion covid 19'
    else:
        Conclusion = 'Debido a que la grafica muestra una pendiente negativa, en el futuro\nprobablemente tendremos una disminucion de los casos confirmados'
    with open ("Reporte25.png","rb") as imagen:
        cadenaBase64 = base64.b64encode(imagen.read())    
    return jsonify({"imagen":cadenaBase64.decode('utf-8'),
                    "grado": R25_Grado_Polinomio, 
                    "RMSE":round(R25_rmse,4),
                    "R2": round(R25_r2,4),
                    "Dias":R25_prediccion,
                    "prediccion":round(R25_pred[0],2),
                    "Conclusion":Conclusion})
                    
@app.route('/Reporte25', methods = ['POST'])
def Reporte25():
    global R25_col_casos, R25_col_fecha, R25_prediccion, R25_Grado_Polinomio, R25_rmse, R25_r2, R25_pred, R25_coeficiente
    VariablesParamR25 = {
        "Variable1":request.json['Variable1'],
        "Variable2":request.json['Variable2'],
        "Variable3":request.json['Variable3']
    }

    R25_col_casos = VariablesParamR25['Variable1']
    R25_col_fecha = VariablesParamR25['Variable2']
    R25_prediccion = VariablesParamR25['Variable3']
    R25_prediccion = float(R25_prediccion)

    Datos = pd.DataFrame(dataset)
    Ejex = []
    Ejey = Datos[R25_col_casos]

    for i in Datos.index:
        Ejex.append(i)
    
    #X = pd.to_datetime(Ejex).astype(np.int64)
    X = np.asarray(Ejex)
    X = X[:,np.newaxis]
    Y = Ejey[:,np.newaxis]
    plt.scatter(X,Y)

    R25_Grado_Polinomio = 3
    Caracteristicas_Polinomio = PolynomialFeatures(degree=R25_Grado_Polinomio)
    Transform_x = Caracteristicas_Polinomio.fit_transform(X)
    modelo = linear_model.LinearRegression().fit(Transform_x,Y)

    nueva_y = modelo.predict(Transform_x)
    
    R25_rmse = np.sqrt(mean_squared_error(Y,nueva_y))
    R25_coeficiente = modelo.coef_[0]
    R25_r2 = r2_score(Y,nueva_y)
    
    x_nuevo_min = 0.0
    x_nuevo_max = R25_prediccion

    x_nuevo = np.linspace(x_nuevo_min,x_nuevo_max,50)
    x_nuevo = x_nuevo[:,np.newaxis]

    x_nuevo_transormado = Caracteristicas_Polinomio.fit_transform(x_nuevo)
    y_nueva = modelo.predict(x_nuevo_transormado)

    obtenerUltimo = np.size(y_nueva)

    R25_pred = y_nueva[obtenerUltimo-1]

    plt.plot(x_nuevo,y_nueva, color ='coral', linewidth = 3)
    plt.grid()

    Titulo = 'Grado = {}; RMSE = {}; \n R2 = {}; \nCon una prediccion para: {} dias \n se tienen aproximadamente = {} Casos confirmados'.format(R25_Grado_Polinomio, R25_rmse, R25_r2, R25_prediccion,R25_pred[0])
    plt.title("Predicción de casos confirmados por día\n " + Titulo, fontsize=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig("Reporte25.png")
    respuesta = jsonify({"message":"variables recibidas","Ver":"Ya puede visualizar el reporte en la seccion de reportes"})
    return respuesta

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
    app.run(debug = True,host='0.0.0.0', port=4000)



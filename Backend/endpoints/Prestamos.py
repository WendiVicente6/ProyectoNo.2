from datetime import datetime, timedelta
import json
from xmlrpc.client import DateTime
import pymongo
import datetime
from time import strftime, localtime
from flask import Blueprint, Response, jsonify, request
multa=-1
Prestamo_service = Blueprint(name="Prestamo_service", import_name=__name__)

@Prestamo_service.route('/verprestamo', methods=['POST','GET'])
def VerPrestamo():
    if request.method == "POST":
        data = request.get_json()
        if "id_lona" in data  :
            if data['id_lona'] != "" :
                prestamo = {
                    "id_lona": data['id_lona'],
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Prestamos"]                  
                    Libro = mongo_collections.find_one({"id_lona": data['id_lona']})
                    if Libro != None:
                        return jsonify({
                            "data": [
                                {
                                "id_lona": Libro.get("id_lona"),
                                "id_book":Libro.get("id_book"),
                                "loan_date":Libro.get("loan_date"),
                                "return_date":Libro.get("return_date"),
                                "id_user":Libro.get("id_user"),
                                }
                            ]
                        }),200
                    else:
                        return jsonify({
                            "mensaje": "Id no encontrado"
                        }),200
                except Exception as e:
                    return jsonify({
                        "estado": "-3",
                        "mensaje": str(e)
                    }),201
            else:
                return jsonify({
                    "estado": "-1",
                    "mensaje": "Petición incorrecta"
                }),201
        else:
            return jsonify({
                "estado": "-1",
                "mensaje": "Petición incorrecta"
            }),201
    else:
        return jsonify({
                "estado": "-1",
                 "mensaje": "Service Unavailable"
            }),201
@Prestamo_service.route('/Registrarprestamos', methods=['POST','GET'])
def RegistrarPrestamo():
    if request.method == "POST":
        data = request.get_json()
        if "id_book" in data and"id_user" in data :
            if data["id_book"] != "" and data["id_user"]:
                generar_prestamo = {
                    "id_book": data['id_book'],
                    "id_user": data['id_user'],
                }

                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    date=datetime.datetime.now()
                    entrega=date+timedelta(days=7)
                    mongo_db = cliente_mongo["store"]
                    mongo_usuario=mongo_db["usuario"] 
                    mongo_libro=mongo_db["Libro"]    
                    mongo_prestamo=mongo_db["Prestamos"]                             
                    buscar_usuario=mongo_usuario.find_one({"id_user":data['id_user']})
                    buscar_libro=mongo_libro.find_one({"id_book":data['id_book']})

                    if buscar_usuario!=None and buscar_libro!= None :                             
                        datos={
                                    "id_lona": 2,
                                    "id_book":buscar_libro.get("id_book"),
                                    "book_title":buscar_libro.get("book_title"),
                                    "book_type":buscar_libro.get("book_type"),
                                    "author":buscar_libro.get("author"),
                                    "book_year":buscar_libro.get("book_year"),
                                    "book_editorial": buscar_libro.get("book_editorial"),
                                    "loan_date":date,
                                    "return_date":entrega,
                                    "id_user":buscar_usuario.get("id_user"),
                                    "user_display_name": buscar_usuario.get("user_display_name"),
                                    "user_career": buscar_usuario.get("user_career"),
                                    "user_carnet": buscar_usuario.get("user_carnet")
                                                                        
                             }
                        presta=mongo_prestamo.insert_one(datos)
                    verpresta=mongo_prestamo.find_one(datos)
                    if verpresta != None:
                        return jsonify({
                            "data": [
                                {
                                "id_lona": verpresta.get("id_lona"),
                                    "id_book":verpresta.get("id_book"),
                                    "book_title":verpresta.get("book_title"),
                                    "book_type":verpresta.get("book_type"),
                                    "author":verpresta.get("author"),
                                    "book_year":verpresta.get("book_year"),
                                    "book_editorial": verpresta.get("book_editorial"),
                                    "loan_date":verpresta.get("loan_date"),
                                    "return_date":verpresta.get("loan_date"),
                                    "id_user":verpresta.get("id_user"),
                                    "user_display_name": verpresta.get("user_display_name"),
                                    "user_career": verpresta.get("user_career"),
                                    "user_carnet": verpresta.get("user_carnet") 
   
                                }
                            ]
                        }),200                   
                    else:
                        return jsonify({
                            "mensaje": "ID no encontrado, verifique que los datos estén correctos"
                        }),200
                except Exception as e:
                    return jsonify({
                        "estado": "-3",
                        "mensaje": str(e)
                    }),201
            else:
                return jsonify({
                    "estado": "-1",
                    "mensaje": "Verifique los datosa"
                }),201
        else:
            return jsonify({
                "estado": "-1",
                "mensaje": "Verifique los datosa"
            }),201
    else:
        return jsonify({
                "estado": "-1",
                 "mensaje": "Service Unavailable"
            }),201
@Prestamo_service.route('/multa', methods=['POST','GET'])
def Multa():
    if request.method == "POST":
        data = request.get_json()
        if "id_lona" in data  :
            if data['id_lona'] != "" :
                prestamo = {
                    "id_lona": data['id_lona'],
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Prestamos"]                  
                    Libro = mongo_collections.find_one({"id_lona": data['id_lona']})
                    
                    if Libro != None:
                        if Libro.get("return_date")<datetime.datetime.now():
                            dias=datetime.datetime.now()-Libro.get("return_date")
                            multa=dias
                            return jsonify({
                                "data": [
                                    {
                                    "id_lona": Libro.get("id_lona"),
                                    "book_title":Libro.get("book_title"),
                                    "loan_date":Libro.get("loan_date"),
                                    "return_date":Libro.get("return_date"),
                                    "user_display_name":Libro.get("user_display_name"),
                                    "penalty_fee":multa,
                                    
                                    }
                                ]
                            }),200
                        else:
                            return jsonify({
                                "data": [
                                    {
                                    "id_lona": Libro.get("id_lona"),
                                    "book_title":Libro.get("book_title"),
                                    "loan_date":Libro.get("loan_date"),
                                    "return_date":Libro.get("return_date"),
                                    "user_display_name":Libro.get("user_display_name"),
                                    "penalty_fee":0,
                                    
                                    }
                                ]
                            }),200
                    else:
                        return jsonify({
                            "mensaje": "Id no encontrado"
                        }),200
                except Exception as e:
                    return jsonify({
                        "estado": "-3",
                        "mensaje": str(e)
                    }),201
            else:
                return jsonify({
                    "estado": "-1",
                    "mensaje": "Verifique los datos"
                }),201
        else:
            return jsonify({
                "estado": "-1",
                "mensaje": "Verifique los datos"
            }),201
    else:
        return jsonify({
                "estado": "-1",
                 "mensaje": "Service Unavailable"
            }),201
import pymongo
from flask import Blueprint, Response, jsonify, request

usuarios_service = Blueprint(name="usuarios_service", import_name=__name__)

@usuarios_service.route('/register', methods=['POST','GET'])
def Registro():
    if request.method == "POST":
        data = request.get_json()
        if "id_user" in data and "user_display_name" in data and "user_nickname" in data and "user_password" in data and "user_age" in data and "user_career" in data and "user_carnet":
            if data["id_user"] != "" and data["user_nickname"] != "" and  data['user_password'] != "" and  data['user_age'] != -1 and  data['user_career'] != "" and data["user_carnet"] != "":
                usuario_insertar = {
                    "id_user":data['id_user'],
                    "user_display_name": data['user_display_name'],
                    "user_nickname": data['user_nickname'],
                    "user_password": data['user_password'],
                    "user_age": data['user_age'],
                    "user_career": data['user_career'],
                    "user_carnet": data['user_carnet']
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["usuario"]
                    respuesta_mongo = mongo_collections.insert_one(usuario_insertar)
                    if respuesta_mongo!=None:
                        return jsonify({
                            "status": 200,
                            "msg": "RESPONSE"
                        }),200
                    else:
                        return jsonify({
                            "estado": 1,
                            "mensaje": "Verifique los datos"
                        }),200
                except Exception as e:
                    return jsonify({
                        "mensaje": e
                    }),201
            else:
                return jsonify({
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

@usuarios_service.route('/login', methods=['POST','GET'])
def Login():
    if request.method == "POST":
        data = request.get_json()
        if "user_nickname" in data and "user_password" :
            if data["user_nickname"] != "" and  data['user_password'] != "":
                usuario_password_query = {
                    "user_nickname": data['user_nickname'],
                    "user_password": data['user_password']
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["usuario"]
                   
                    usuario = mongo_collections.find_one(usuario_password_query)
                    respuesta_mongo=mongo_collections.insert_one(usuario_password_query)
                    if usuario != None:
                        return jsonify({
                            "estado": 1,
                            "data": [
                                {
                                    "id_user": usuario.get("id_user"),
                                    "user_display_name": usuario.get("user_display_name"),
                                    "user_nickname":usuario.get("user_nickname"),
                                    "user_password":usuario.get("user_password"),
                                    "user_age":usuario.get("user_age"),
                                    "user_career": usuario.get("user_career"),
                                    "user_carnet": usuario.get("user_carnet")
                                }
                            ]
                        }),200
                    else:
                        return jsonify({
                            "estado": 1,
                            "mensaje": "Datos Incorrectos"
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

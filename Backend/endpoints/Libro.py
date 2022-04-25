import pymongo
from flask import Blueprint, Response, jsonify, request

Libro_service = Blueprint(name="Libro_service", import_name=__name__)

@Libro_service.route('/register', methods=['POST','GET'])
def Registro():
    if request.method == "POST":
        data = request.get_json()
        if "id_book" in data and"book_title" in data and "book_type" in data and "author" in data and "book_count" in data and "book_available" in data and "book_not_available" in data and "book_year" in data and "book_editorial":
            if data["id_book"] != "" and data["book_title"] != "" and  data["book_type"] != "" and data["author"] != "" and  data['book_count'] != -1 and data['book_available'] != -1 and data['book_not_available'] != -1 and data['book_year'] != -1 and data["book_editorial"] != "" :
                usuario_insertar = {
                    "id_book": data['id_book'],
                    "book_title": data['book_title'],
                    "book_type": data['book_type'],
                    "author": data['author'],
                    "book_count": data['book_count'],
                    "book_available": data['book_available'],
                    "book_not_available": data['book_not_available'],
                    "book_year": data['book_year'],
                    "book_editorial": data['book_editorial']
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Libro"]
                    respuesta_mongo = mongo_collections.insert_one(usuario_insertar)
                    return jsonify({
                        "status": 200,
                        "msg": "RESPONSE"
                    }),200
                except Exception as e:
                    return jsonify({
                        "estado": "-3",
                        "mensaje": e
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

@Libro_service.route('/verlibro', methods=['POST','GET'])
def VerLibro():
    if request.method == "POST":
        data = request.get_json()
        if "id_book" in data and "book_type" in data and "book_title" :
            if data["id_book"] != "" and  data["book_type"] != "" and  data["book_title"] != "":
                usuario_password_query = {
                    "id_book": data['id_book'],
                    "book_type": data['book_type'],
                    "book_title": data['book_title']
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Libro"]                  
                    Libro = mongo_collections.find_one(usuario_password_query)
                    if Libro != None:
                        return jsonify({
                            "data": [
                                {
                                "id_book": Libro.get("id_book"),
                                "book_title":Libro.get("book_title"),
                                "book_type":Libro.get("book_type"),
                                "author":Libro.get("author"),
                                "book_count":Libro.get("book_count"),
                                "book_available": Libro.get("book_available"),
                                "book_not_available":Libro.get("book_not_available"),
                                "book_year":Libro.get("book_year"),
                                "book_editorial": Libro.get("book_editorial")     
                                }
                            ]
                        }),200
                    else:
                        return jsonify({
                            "estado": 1,
                            "mensaje": "Usuario y/o Contraseña incorrectos"
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
@Libro_service.route('/ActualizarLibro', methods=['POST','GET'])
def ActualizarLibro():
    if request.method == "POST":
        data = request.get_json()
        if "id_book" in data and"book_title" in data and "book_type" in data and "author" in data and "book_count" in data and "book_available" in data and "book_not_available" in data and "book_year" in data and "book_editorial":
            if data["id_book"] != "" and data["book_title"] != "" and  data["book_type"] != "" and data["author"] != "" and  data['book_count'] != -1 and data['book_available'] != -1 and data['book_not_available'] != -1 and data['book_year'] != -1 and data["book_editorial"] != "" :
                usuario_insertar = {
                    "id_book": data['id_book'],
                    "book_title": data['book_title'],
                    "book_type": data['book_type'],
                    "author": data['author'],
                    "book_count": data['book_count'],
                    "book_available": data['book_available'],
                    "book_not_available": data['book_not_available'],
                    "book_year": data['book_year'],
                    "book_editorial": data['book_editorial']
                }

                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Libro"]                                  
                    Libroactualizado=mongo_collections.update_one({"id_book":data['id_book']},{"$set":usuario_insertar})
                    Libro = mongo_collections.find_one({"id_book":data['id_book']})
                    if Libro != None:
                        return jsonify({
                            "data": [
                                {
                               "status": 200,
                                "msg": "response"  
   
                                }
                            ]
                        }),200
                    else:
                        return jsonify({
                            "mensaje": "ID no encontrado"
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
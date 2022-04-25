from flask import Blueprint, jsonify, request, Response
import pymongo

productos_service = Blueprint(name="productos_service", import_name=__name__)

@productos_service.route('/nuevoproducto', methods=['POST','GET','PUT'])
def RegistroProducto():
    if request.method == "POST":
        data = request.get_json()
        if "codigo" in data and "nombre" in data and "precio" in data and "qty" in data :
            if data["codigo"] != "" and  data['nombre'] != "" and  data['precio'] != -1 and  data['qty'] != -1:
                producto_insertar = {
                    "codigo": data['codigo'],
                    "nombre": data['nombre'],
                    "precio": data['precio'],
                    "qty": data['qty']
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["producto"]
                    respuesta_mongo = mongo_collections.insert_one(producto_insertar)
                    return jsonify({
                        "estado": "1",
                        "mensaje": "Datos insertados correctamente, ID: " + str(respuesta_mongo.inserted_id)
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

@productos_service.route('/obtenerproductos', methods=['POST','GET','PUT'])
def BuscarProducto():
    if request.method == "GET":
        producto_query = { "qty": {"$gt": 0}}
        try:
            cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
            mongo_db = cliente_mongo["store"]
            mongo_collections = mongo_db["producto"]
            respuesta_mongo = mongo_collections.find(producto_query)
            respuesta_mongo.sort("nombre")
            productos = []
            for producto in respuesta_mongo:
                productos.append(
                    {
                        "codigo": producto.get("codigo"),
                        "nombre": producto.get('nombre'),
                        "precio": producto.get('precio'),
                        "qty": producto.get('qty')
                    }
                )
            return jsonify({
                "estado": 1,
                "data": productos
            }),200
        except Exception as e:
            return jsonify({
                "estado": "-3",
                "mensaje": e
            }),201
    else:
        return jsonify({
                "estado": "-1",
                 "mensaje": "Service Unavailable"
            }),201


@productos_service.route('/obtenerproductos/busqueda', methods=['POST','GET','PUT'])
def BuscarProductoEspecifico():
    if request.method == "GET":
        data = request.get_json()
        if "precio" in data:
            precio = int(str(data["precio"]))
            producto_query = { "precio": {"$gte": precio}}
            try:
                cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                mongo_db = cliente_mongo["store"]
                mongo_collections = mongo_db["producto"]
                respuesta_mongo = mongo_collections.find(producto_query)
                respuesta_mongo.sort("nombre")
                productos = []
                if respuesta_mongo != None:
                    for producto in respuesta_mongo:
                        productos.append(
                            {
                                "codigo": producto.get("codigo"),
                                "nombre": producto.get('nombre'),
                                "precio": producto.get('precio'),
                                "qty": producto.get('qty')
                            }
                        )
                return jsonify({
                    "estado": 1,
                    "data": productos
                }),200
            except Exception as e:
                return jsonify({
                    "estado": "-3",
                    "mensaje": e
                }),201
        elif "nombre" in data:
            nombre = str(data["nombre"])
            try:
                cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                mongo_db = cliente_mongo["store"]
                mongo_collections = mongo_db["producto"]
                respuesta_mongo = mongo_collections.find()
                respuesta_mongo.sort("nombre")
                productos = []
                if respuesta_mongo != None:
                    for producto in respuesta_mongo:
                        if producto.get('nombre').find(nombre) != -1:
                            productos.append(
                                {
                                    "codigo": producto.get("codigo"),
                                    "nombre": producto.get('nombre'),
                                    "precio": producto.get('precio'),
                                    "qty": producto.get('qty')
                                }
                            )
                return jsonify({
                    "estado": 1,
                    "data": productos
                }),200
            except Exception as e:
                return jsonify({
                    "estado": "-3",
                    "mensaje": e
                }),201
        elif "qty" in data:
            qty = int(str(data["qty"]))
            producto_query = { "qty": {"$gte": qty}}
            try:
                cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                mongo_db = cliente_mongo["store"]
                mongo_collections = mongo_db["producto"]
                respuesta_mongo = mongo_collections.find(producto_query)
                respuesta_mongo.sort("nombre")
                productos = []
                if respuesta_mongo != None:
                    for producto in respuesta_mongo:
                        productos.append(
                            {
                                "codigo": producto.get("codigo"),
                                "nombre": producto.get('nombre'),
                                "precio": producto.get('precio'),
                                "qty": producto.get('qty')
                            }
                        )
                return jsonify({
                    "estado": 1,
                    "data": productos
                }),200
            except Exception as e:
                return jsonify({
                    "estado": "-3",
                    "mensaje": e
                }),201
        else:
            return jsonify({
                "estado": "-1",
                 "mensaje": "Solicitud incorrecta"
            }),201
        
    else:
        return jsonify({
                "estado": "-1",
                 "mensaje": "Service Unavailable"
            }),201

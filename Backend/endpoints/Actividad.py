from datetime import date, datetime, timedelta
import pymongo
from flask import Blueprint, Response, jsonify, request
import datetime
Actividad_service = Blueprint(name="Actividad_service", import_name=__name__)

@Actividad_service.route('/crear', methods=['POST','GET'])
def Registro():
    if request.method == "POST":
        data = request.get_json()
        if "Dentro de cuantos días desea la actividad" in data and "NombreActividad" in data and "DescripciónActividad" in data and  "CantidadPersonas" in data:
            if data["Dentro de cuantos días desea la actividad"] != -1 and data["NombreActividad"] != "" and data["DescripciónActividad"] != "" and data["CantidadPersonas"] != -1 :
                usuario_insertar = {
                    "Dentro de cuantos días desea la actividad":data['Dentro de cuantos días desea la actividad'],
                    "NombreActividad": data['NombreActividad'],
                    "DescripciónActividad": data['DescripciónActividad'],
                    "CantidadPersonas": data['CantidadPersonas'],
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Actividad"]
                    respuesta_mongo = mongo_collections.insert_one(usuario_insertar)
                    buscar=mongo_collections.find_one({"NombreActividad":data['NombreActividad']})
                    if buscar != None:
                        hora=buscar.get("Dentro de cuantos días desea la actividad")
                        hoy=datetime.datetime.now()
                        td=timedelta(days=hora)
                        tiempo=hoy+td
                        return jsonify({
                                "data": [
                                    {
                                    "NombreActividad": buscar.get("NombreActividad"),
                                    "DescripciónActividad":buscar.get("DescripciónActividad"),
                                    "CantidadPersonas":buscar.get("CantidadPersonas"),
                                    "Fecha Programada":tiempo


                                    
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

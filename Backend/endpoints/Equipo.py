from datetime import date, datetime, timedelta
import pymongo
from flask import Blueprint, Response, jsonify, request
import datetime
Equipo_service = Blueprint(name="Equipo_service", import_name=__name__)

@Equipo_service.route('/registroequipos', methods=['POST','GET'])
def Registro():
    if request.method == "POST":
        data = request.get_json()
        if "carnet" in data and "Time" in data and "No_equipo" in data:
            if data["carnet"] != "" and data['Time'] != -1  and data['No_equipo'] != -1:
                usuario_insertar = {
                    "carnet":data['carnet'],
                    "Time": data['Time'],
                    "No_equipo": data['No_equipo'],
                }
                try:
                    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
                    mongo_db = cliente_mongo["store"]
                    mongo_collections = mongo_db["Equipo"]
                    respuesta_mongo = mongo_collections.insert_one(usuario_insertar)
                    buscar=mongo_collections.find_one({"carnet":data['carnet']})
                    if buscar != None:
                        hora=buscar.get("Time")
                        hoy=datetime.datetime.now()
                        td=timedelta(hours=hora)
                        tiempo=hoy+td
                        return jsonify({
                                "data": [
                                    {
                                    "carnet": buscar.get("carnet"),
                                    "Time":buscar.get("Time"),
                                    "No_equipo":buscar.get("No_equipo"),
                                    "Entrada":hoy,
                                    "Salida":tiempo


                                    
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
                 "mensaje": "Verifique los datos"
            }),201


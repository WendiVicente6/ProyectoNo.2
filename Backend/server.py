##IMPORTS
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

## LLAMADAS ENPOINTS

from endpoints.usuarios import usuarios_service
from endpoints.productos import productos_service
from endpoints.Libro import Libro_service
from endpoints.Prestamos import Prestamo_service
from endpoints.Equipo import Equipo_service
from endpoints.Actividad import Actividad_service

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")

##ENDPOINTS 
""" Blueprint
    Tienda de conveniencia

    -> usuarios -> (Cajeros, Supervisores)
    -> productos
    -> ventas

    --------------------- usuarios
    {
        "user_display_name": "Wendi Vicente",
        "user_nickname": "Wendi612",
        "user_password":"123456",
        "user_age":21,
        "user_career": "Ingeniería en Ciencias y sistemas",
        "user_carnet": 202106484
    }

    -------------------- productos
    {
        "id_book": "6264dda386dcec77ccb0e111",
                                    "book_title":Libro.get("book_title"),
                                    "book_type":Libro.get("book_type"),
                                    "author":Libro.get("author"),
                                    "book_count":Libro.get("book_count"),
                                    "book_available": Libro.get("book_available"),
                                    "book_not_available":Libro.get("book_not_available"),
                                    "book_year":Libro.get("book_year"),
                                    "book_editorial": Libro.get("book_editorial")
    }

    ------------------- ventas
    {
        "Fecha": "14/05/2022",
        "NoFactura": 1,
        "Nit": "1123",
        "Nombre Cliente": "",
        "Nombre Cajero": "",
        "Productos" : [
            {
                "Codigo": "",
                "Cantidad": 5,
                "Subtotal": 55
            }
        ],
        "Total": 1500
    }

"""

app.register_blueprint(usuarios_service, url_prefix="/api/v1/usuarios")
app.register_blueprint(productos_service, url_prefix="/api/v1/productos")
app.register_blueprint(Libro_service, url_prefix="/api/v1/Libro")
app.register_blueprint(Prestamo_service, url_prefix="/api/v1/Prestamos")
app.register_blueprint(Equipo_service, url_prefix="/api/v1/Equipos")
app.register_blueprint(Actividad_service, url_prefix="/api/v1/Actividades")

##ENDPOINTS
@app.route('/', methods = ['GET','POST','PUT'])
def init():
     return jsonify({
        "Proyecto"    : "Proyecto NO. 2 BIBLIOTECA"
    })

## INIT
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='3000', debug = True)


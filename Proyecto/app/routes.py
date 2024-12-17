from flask import Blueprint, jsonify, render_template
from .services.starship_service import StarshipService
from .services.pilot_service import PilotService
from .services.VehicleService import VehicleService


bp = Blueprint('api', __name__)

# Ruta para la página de inicio
@bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

def register_routes(app):
    app.register_blueprint(bp, url_prefix='/api') 
    
@bp.route('/api/nave/general', methods=['GET'])
def get_general_starships():
    service = StarshipService()  # Instanciamos el servicio
    data = service.get_general_starships()  # Método para obtener naves generales
    return jsonify(data) 



# Ruta para obtener la nave específica
@bp.route('/api/nave/especifico/', methods=['GET'])
def get_specific_starship():
    service = VehicleService()  # Instanciamos el servicio
    data = service.get_all_vehicles()  # Llamamos al método con el ID de la nave
    return jsonify(data)  # Retornamos los datos

# Ruta para obtener los detalles del piloto
@bp.route('/api/nave/piloto', methods=['GET']) 
def get_pilot_details():
    service = PilotService()  # Instanciamos el servicio de pilotos
    data = service.get_pilot_details()  # Llamamos al método para obtener todos los pilotos
    return jsonify(data)





# Ruta para actualizar la nave
@bp.route('/api/nave/objeto_nave', methods=['GET'])
def get_all_vehicles():
    service = VehicleService()  # Crear una instancia de VehicleService
    data = service.get_all_vehicles()  # Llamar al método get_all_vehicles() de la instancia
    return jsonify(data)  # Retornar los datos en formato JSON



def register_routes(app):
    app.register_blueprint(bp)
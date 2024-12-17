import requests

class VehicleService:
    BASE_URL = "https://swapi.py4e.com/api/vehicles/"

    def get_all_vehicles(self):

        # Obtiene la información de todos los vehículos disponibles en la API.
        all_vehicles = []
        next_url = self.BASE_URL  # Iniciar con la URL base
        
        while next_url:  # Mientras haya una URL en 'next', continuar solicitando
            response = requests.get(next_url)
            
            if response.status_code == 200:
                data = response.json()
                vehicles = data.get("results", [])  # Obtener los resultados (vehículos de la página)
                all_vehicles.extend(self.extract_vehicle_data(vehicles))  # Extraer y agregar la información
                next_url = data.get("next")  # Obtener la URL de la siguiente página
            else:
                print(f"Error al obtener los datos: {response.status_code}")
                break
        
        return all_vehicles

    def extract_vehicle_data(self, vehicles):
        # Extrae y organiza la información relevante de los vehículos.
        extracted_data = []
        for vehicle in vehicles:
            vehicle_info = {
                "Nombre": vehicle.get("name", "Desconocido"),
                "Modelo": vehicle.get("model", "Desconocido"),
                "Costo": vehicle.get("cost_in_credits", "Desconocido"),
                "Velocidad máxima": vehicle.get("max_atmosphering_speed", "Desconocido"),
                "Capacidad de tripulación": vehicle.get("crew", "Desconocido"),
                "Capacidad de pasajeros": vehicle.get("passengers", "Desconocido"),
                "Pilotos": self.get_pilots(vehicle.get("pilots", [])),
            }
            extracted_data.append(vehicle_info)
        return extracted_data
    

    def get_pilots(self, pilot_urls):
        # Obtiene el total y los nombres de los pilotos asignados a partir de sus URLs GENERAADAS 1/2/3/4/6 ETC.
        pilots = []
        for pilot_url in pilot_urls:
            response = requests.get(pilot_url)
            if response.status_code == 200:
                pilot_data = response.json()
                pilots.append(pilot_data.get("name", "Desconocido"))
            else:
                pilots.append("Desconocido")
        return {"Total de pilotos": len(pilots), "Nombres": pilots}


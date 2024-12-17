import requests

class StarshipService:
    API_URLS = "https://swapi.py4e.com/api/starships/"
    API_URLP = "https://swapi.py4e.com/api/people/"

# #### corregido ok API Nave General (Java/Python)
    def get_general_starships(self):
        response = requests.get(self.API_URLS)  # Hacemos una solicitud GET a la API de Star Wars
        if response.status_code == 200:
            starships = response.json().get('results', [])  # Obtenemos la lista de naves
            return [
                {
                    "Nombre de la nave": ship.get("name"),
                    "Modelo": ship.get("model"),
                    "Costo": ship.get("cost_in_credits"),
                    "Velocidad": ship.get("max_atmosphering_speed"),
                }
                for ship in starships
            ]
        return []  # Si la respuesta no es exitosa, devolvemos una lista vacía
    
############  API Nave Especifico (Java/Python)  
    def get_specific_starship(self):
        response = requests.get(self.API_URLS)  # Hacemos una solicitud GET a la API de Star Wars
        if response.status_code == 200:
            starships = response.json().get('results', [])  # Obtenemos la lista de naves
            return [
                {
                    "Nombre de la nave": ship.get("name"),
                    "Modelo": ship.get("model"),
                    "Costo": ship.get("cost_in_credits"),
                    "Velocidad": ship.get("max_atmosphering_speed"),
                    "Capacidad de carga de personal": ship.get("crew"),
                    "Capacidad de carga de pasajeros": ship.get("passengers"),
                    
                }
                for ship in starships
            ]
        return []  
    
    # Método para obtener naves y los detalles de los pilotos asociados
    def get_starships_with_pilots(self):
        starships_with_pilots = []
        response = requests.get(self.API_URLS)
        if response.status_code == 200:
            starships = response.json().get('results', [])
            for starship in starships:
                starship_data = {
                    "Nombre de la nave": starship.get("name"),
                    "Modelo": starship.get("model"),
                    "Pilotos": []
                }
                # Obtenemos los pilotos asociados a la nave
                pilots = starship.get("pilots", [])
                for pilot_url in pilots:
                    pilot_service = PilotService()
                    pilot_data = pilot_service.get_pilot_details_from_url(pilot_url)
                    starship_data["Pilotos"].append(pilot_data)
                
                starships_with_pilots.append(starship_data)

        return starships_with_pilots

# CREACION CLASE PILOTO PARA OBTENER LOS DATOS 
class Pilotos:
    API_URL_PEOPLE = "https://swapi.py4e.com/api/people/"
    
    def __init__(self):
        self.pilots_data = []

    def get_all_pilots(self):
        next_url = self.API_URL_PEOPLE
        while next_url:
            response = requests.get(next_url)
            if response.status_code == 200:
                data = response.json()
                next_url = data.get("next")  # Continuar a la siguiente página si existe
                self.extract_pilot_details(data["results"])
            else:
                print(f"Error al obtener datos: {response.status_code}")
                break
        return self.pilots_data

    def extract_pilot_details(self, pilots):
        for pilot in pilots:
            pilot_data = {
                "Nombre": pilot.get("name"),
                "Altura": pilot.get("height"),
                "Género": pilot.get("gender"),
                "Peso": pilot.get("mass"),
                "Año de nacimiento": pilot.get("birth_year"),
                "Nombre de la especie": self.get_species_names(pilot.get("species")),
                "Vehículos pilotados": self.get_vehicle_names(pilot.get("vehicles")),
                "Planeta de origen": self.get_homeworld_name(pilot.get("homeworld"))
            }
            self.pilots_data.append(pilot_data)

    def get_species_names(self, species_urls):
        species_names = []
        for species_url in species_urls:
            response = requests.get(species_url)
            if response.status_code == 200:
                species_names.append(response.json().get("name", "Desconocido"))
        return species_names if species_names else ["Desconocido"]

    def get_vehicle_names(self, vehicle_urls):
        vehicle_names = []
        for vehicle_url in vehicle_urls:
            response = requests.get(vehicle_url)
            if response.status_code == 200:
                vehicle_names.append(response.json().get("name", "Desconocido"))
        return vehicle_names if vehicle_names else ["Desconocido"]

    def get_homeworld_name(self, homeworld_url):
        if homeworld_url:
            response = requests.get(homeworld_url)
            if response.status_code == 200:
                return response.json().get("name", "Desconocido")
        return "Desconocido"

# # Ejemplo de uso
# if __name__ == "__main__":
#     pilotos_service = Pilotos()
#     pilotos_data = pilotos_service.get_all_pilots()
    
#     # Imprimir el resultado
#     for pilot in pilotos_data:
#         print(pilot)
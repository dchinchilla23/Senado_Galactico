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
class PilotService:
    def get_pilot_details(self):
        pilots = []
        url = StarshipService.API_URLP  # Usamos la URL de pilotos de StarshipService

        while url:
            response = requests.get(url)
            if response.status_code == 200:
                pilot_data = response.json().get('results', [])
                pilots.extend(pilot_data)
                url = response.json().get('next')
            else:
                return {"error": "No se pudieron obtener los detalles de los pilotos."}

        ordered_data = [
            {
                "Nombre": pilot.get("name"),
                "Altura": pilot.get("height"),
                "Género": pilot.get("gender"),
                "Peso": pilot.get("mass"),
                "Año de nacimiento": pilot.get("birth_year"),
                "Nombre de la especie": self.get_species_name(pilot.get("species")),
                "Vehículos pilotados": self.get_vehicles_names(pilot.get("vehicles")),
                "Planeta de origen": self.get_homeworld_name(pilot.get("homeworld"))
            }
            for pilot in pilots
        ]
        return ordered_data

    def get_pilot_details_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pilot = response.json()
            return {
                "Nombre": pilot.get("name"),
                "Género": pilot.get("gender"),
                "Año de nacimiento": pilot.get("birth_year"),
                "Altura": pilot.get("height"),
                "Peso": pilot.get("mass")
            }
        return {}

    def get_species_name(self, species_urls):
        species_names = []
        for species_url in species_urls:
            response = requests.get(species_url)
            if response.status_code == 200:
                species_names.append(response.json().get("name", "Desconocido"))
        return species_names if species_names else ["Desconocido"]

    def get_vehicles_names(self, vehicles_urls):
        vehicles = []
        for vehicle_url in vehicles_urls:
            response = requests.get(vehicle_url)
            if response.status_code == 200:
                vehicles.append(response.json().get("name", "Desconocido"))
        return vehicles

    def get_homeworld_name(self, homeworld_url):
        if homeworld_url:
            response = requests.get(homeworld_url)
            if response.status_code == 200:
                return response.json().get("name", "Desconocido")
        return "Desconocido"

# Uso del código
starship_service = StarshipService()
starships_with_pilots = starship_service.get_starships_with_pilots()

for starship in starships_with_pilots:
    print(f"Nave: {starship['Nombre de la nave']} - Modelo: {starship['Modelo']}")
    if starship['Pilotos']:
        for pilot in starship['Pilotos']:
            print(f"  Piloto: {pilot['Nombre']} - Género: {pilot['Género']} - Año de nacimiento: {pilot['Año de nacimiento']}")
    else:
        print("  No tiene pilotos asignados.")
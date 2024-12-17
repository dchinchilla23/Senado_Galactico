import requests

class PilotService:
    def get_pilot_details(self):
        # Aquí va la lógica para obtener los detalles del piloto
        response = requests.get("https://swapi.py4e.com/api/people/1/")
        if response.status_code == 200:
            pilot_data = response.json()
            return {
                "Nombre": pilot_data.get("name"),
                "Altura": pilot_data.get("height"),
                "Género": pilot_data.get("gender"),
                "Peso": pilot_data.get("mass"),
                "Año de nacimiento": pilot_data.get("birth_year"),
                "Nombre de la especie": self.get_species_name(pilot_data.get("species")),
                "Vehículos pilotados": self.get_vehicles_names(pilot_data.get("vehicles")),
                "Planeta de origen": self.get_homeworld_name(pilot_data.get("homeworld"))
            }
        return {}

    def get_species_name(self, species_url_list):
        species_names = []
        for species_url in species_url_list:
            if species_url:
                species_response = requests.get(species_url)
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    species_names.append(species_data.get("name", "Desconocido"))
        return species_names if species_names else ["Desconocido"]
    
    def get_vehicles_names(self, vehicles_url_list):
        vehicle_names = []
        for vehicle_url in vehicles_url_list:
            if vehicle_url:
                vehicle_response = requests.get(vehicle_url)
                if vehicle_response.status_code == 200:
                    vehicle_data = vehicle_response.json()
                    vehicle_names.append(vehicle_data.get("name", "Desconocido"))
        return vehicle_names if vehicle_names else ["Ninguno"]
    
    def get_homeworld_name(self, homeworld_url):
        if homeworld_url:
            homeworld_response = requests.get(homeworld_url)
            if homeworld_response.status_code == 200:
                homeworld_data = homeworld_response.json()
                return homeworld_data.get("name", "Desconocido")
        return "Desconocido"

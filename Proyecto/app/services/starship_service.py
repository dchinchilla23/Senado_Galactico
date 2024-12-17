import requests

class StarshipService:
    API_URLS = "https://swapi.py4e.com/api/starships/"
    API_URLP = "https://swapi.py4e.com/api/people/"
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
# #### corregido ok API Nave General (Java/Python)
    
    
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

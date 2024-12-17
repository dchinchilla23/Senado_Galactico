import requests

class PilotService:
    BASE_URL = "https://swapi.py4e.com/api/people/"

    def get_pilot_details(self):
        # CONSULTA Recorre  todas las páginas de la API /people/ y obtiene la información de todos los pilotos.

        all_pilots = []
        next_url = self.BASE_URL  # Iniciar con la URL base
        
        while next_url:  # Mientras haya una URL en 'next', continuar solicitando
            response = requests.get(next_url)
            
            if response.status_code == 200:
                data = response.json()
                pilots = data.get("results", [])  # Obtener los resultados (pilotos de la página)
                all_pilots.extend(self.extract_pilot_data(pilots))  # Extraer y agregar la información
                next_url = data.get("next")  # Obtener la URL de la siguiente página
            else:
                print(f"Error al obtener los datos: {response.status_code}")
                break
        
        return all_pilots

    def extract_pilot_data(self, pilots):
        # Extrae y organiza la información relevante de los pilotos.
        extracted_data = []
        for pilot in pilots:
            pilot_info = {
                "Nombre": pilot.get("name"),
                "Altura": pilot.get("height"),
                "Peso": pilot.get("mass"),
                "Género": pilot.get("gender"),
                "Planeta de origen": self.get_homeworld(pilot.get("homeworld")),
                "Vehículos": self.get_details_from_urls(pilot.get("vehicles")),
                "Naves": self.get_details_from_urls(pilot.get("starships")),
                "Nombre de la especie": self.get_details_from_urls(pilot.get("species")),
            }
            extracted_data.append(pilot_info)
        return extracted_data

    def get_homeworld(self, url):
        # Obtiene el nombre del planeta de origen desde una URL.
        if not url:
            return "Desconocido"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("name", "Desconocido")
        return "Desconocido"

    def get_details_from_urls(self, urls):
        # Recorre una lista de URLs y extrae nombres de recursos (vehículos, naves, especies, películas).
        names = []
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                name = response.json().get("name") or response.json().get("title")
                names.append(name if name else "Desconocido")
        return names if names else ["Ninguno"]

    
    def display_paginated_pilots(self, pilots, page_size=10):
        # Muestra la información de los pilotos en bloques de tamaño fijo PAGINACIOIN.
        total_pilots = len(pilots)
        start = 0

        while start < total_pilots:
            end = min(start + page_size, total_pilots)
            print(f"Mostrando pilotos {start + 1} a {end} de {total_pilots}")
            print("-" * 40)

            for i, pilot in enumerate(pilots[start:end], start=start + 1):
                print(f"Piloto {i}:")
                for key, value in pilot.items():
                    print(f"  {key}: {value}")
                print("-" * 40)
            
            start += page_size

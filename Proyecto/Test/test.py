import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import unittest
from unittest.mock import patch, MagicMock
# from app.services.pilot_service import PilotService  # Asegúrate de que la ruta de importación sea correcta
from app.services.pilot_service import PilotService
class TestPilotService(unittest.TestCase):

    @patch('app.services.pilot_service.requests.get')  # Mockeamos requests.get
    def test_get_pilot_details(self, mock_get):
        # Simulamos la respuesta de la API para la primera página de pilotos
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"name": "Luke Skywalker", "height": "172", "mass": "77", "gender": "male", "homeworld": "https://swapi.py4e.com/api/planets/1/", "vehicles": [], "starships": [], "species": []},
                {"name": "C-3PO", "height": "167", "mass": "75", "gender": "n/a", "homeworld": "https://swapi.py4e.com/api/planets/1/", "vehicles": [], "starships": [], "species": []}
            ],
            "next": None  # No hay más páginas
        }
        mock_get.return_value = mock_response

        # Crear una instancia de PilotService y llamar al método get_pilot_details
        service = PilotService()
        pilots = service.get_pilot_details()

        # Verificar que la respuesta contiene los pilotos esperados
        self.assertEqual(len(pilots), 2)
        self.assertEqual(pilots[0]['Nombre'], 'Luke Skywalker')
        self.assertEqual(pilots[1]['Nombre'], 'C-3PO')

    @patch('app.pilot_service.requests.get')  # Mockeamos requests.get
    def test_get_homeworld(self, mock_get):
        # Simulamos la respuesta para obtener el planeta de origen
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Tatooine"}
        mock_get.return_value = mock_response

        # Crear una instancia de PilotService
        service = PilotService()

        # Llamar al método get_homeworld con una URL simulada
        homeworld = service.get_homeworld("https://swapi.py4e.com/api/planets/1/")

        # Verificar que el planeta de origen sea el esperado
        self.assertEqual(homeworld, "Tatooine")

    @patch('app.pilot_service.requests.get')  # Mockeamos requests.get
    def test_get_details_from_urls(self, mock_get):
        # Simulamos la respuesta para obtener detalles de vehículos o naves
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Speeder Bike"}
        mock_get.return_value = mock_response

        # Crear una instancia de PilotService
        service = PilotService()

        # Llamar al método get_details_from_urls con una URL simulada
        details = service.get_details_from_urls(["https://swapi.py4e.com/api/vehicles/30/"])

        # Verificar que el nombre del vehículo/nave sea el esperado
        self.assertEqual(details, ["Speeder Bike"])

    def test_display_paginated_pilots(self):
        # Datos simulados de pilotos para la paginación
        pilots = [
            {"Nombre": "Luke Skywalker", "Modelo": "X-wing", "Costo": "2000"},
            {"Nombre": "C-3PO", "Modelo": "Protocol droid", "Costo": "null"}
        ]

        service = PilotService()

        # Capturar la salida impresa en consola
        with self.assertLogs('app.pilot_service', level='INFO') as log:
            service.display_paginated_pilots(pilots, page_size=1)

        # Verificar que la paginación muestra la información de los pilotos correctamente
        self.assertIn("Mostrando pilotos 1 a 1", log.output[0])
        self.assertIn("Piloto 1:", log.output[1])

if __name__ == '__main__':
    unittest.main()

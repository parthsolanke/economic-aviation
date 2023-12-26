import os
import requests
from flight_data import FlightData

KIWI_ENDPT = "https://tequila-api.kiwi.com"
KIWI_API_KEY = os.environ.get("KIWI_API_KEY")

class FlightSearch:
    '''
    This class is responsible for searching flights and returning IATA codes.
    '''
    def get_iata_code(self, city):
        api_key = {
            "apikey": KIWI_API_KEY
        }
        params = {
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=f"{KIWI_ENDPT}/locations/query",
                                params=params, headers=api_key)
        response.raise_for_status()
        code = response.json()["locations"][0]["code"]
        return code
    
    def search_flights(self, 
                       origin_city_code,
                       destination_city_code,
                       from_time,
                       to_time):
        api_key = {
            "apikey": KIWI_API_KEY
        }
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "INR"
        }
        response = requests.get(url=f"{KIWI_ENDPT}/v2/search",
                                params=params, headers=api_key)
        
        # checking if flights are available
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        
        flight_info = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_info.destination_city}: ₹{flight_info.price}")
        return flight_info
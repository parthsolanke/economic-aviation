import requests

SHEETY_ENDPT = "https://api.sheety.co/acea441ee1f58656db9770ee62b22517/economicAviation/prices"
class DataManager:
    '''
    This class is responsible for talking to the Google Sheet.
    '''
    def __init__(self):
        self.data = {}
        
    def get_data(self):
        response = requests.get(url=SHEETY_ENDPT)
        response.raise_for_status()
        sheet = response.json()
        self.data = sheet["prices"]
        return self.data
        
    def update_sheet(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            
            response = requests.put(
                url=f"{SHEETY_ENDPT}/{city['id']}",
                json=new_data
            )
            response.raise_for_status()
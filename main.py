from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch

flight_search = FlightSearch()
data_man = DataManager()
sheet = data_man.get_data()
ORIGIN_CITY_IATA = "LON"

# searchinga and updating iata codes in the sheet
for dict in sheet:
    if dict["iataCode"] == "":
        dict["iataCode"] = flight_search.get_iata_code(dict["city"])
data_man.data = sheet
data_man.update_sheet()

# searching for flights
today = datetime.now()
six_months = today + timedelta(days=180)

for dict in sheet:
    flight = flight_search.search_flights(
        ORIGIN_CITY_IATA,
        dict["iataCode"],
        today,
        six_months
    )
    if flight.price < dict["lowestPrice"]:
        print(f"Low price alert! Only ₹{flight.price}"\
              f" to fly from {flight.origin_city}-{flight.origin_airport}"\
              f" to {flight.destination_city}-{flight.destination_airport},"\
              f" from {flight.out_date} to {flight.return_date}.")
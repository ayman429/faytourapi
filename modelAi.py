import requests


place_response = 'https://faytourapp.pythonanywhere.com/api/TourismPlace/'
place_headers = {
    'Authorization': 'Token 9500d4298aba1a2446229d75a0e5794e9209c667'
}
# print(place_response_obj)
# print("====>"+place_response)
place_response_obj = requests.get(
    place_response, headers=place_headers)
# if place_response_obj.status_code == 200:
print("======================")
print(place_response_obj.json())
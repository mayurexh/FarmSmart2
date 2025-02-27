import requests
from django.http import JsonResponse
from django.shortcuts import render

API_KEY = "579b464db66ec23bdd0000011bf984110a85423f69e470716ba32d66"
API_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"

def market_prices_page(request):
    return render(request, "marketprices/compare.html")

def search_prices(request):
    state = request.GET.get("state", "").strip()
    district = request.GET.get("district", "").strip()
    commodity = request.GET.get("commodity", "").strip()
    arrival_date = request.GET.get("arrival_date", "").strip()
    print(state, district, commodity, arrival_date)

    if not state or not district or not commodity:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    # API request parameters
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 10,
        "filters[State.keyword]": state,
        "filters[District.keyword]": district,
        "filters[Commodity.keyword]": commodity,
        "filters[Arrival_Date]":arrival_date
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse({"records": data.get("records", [])}, safe=False)
    
    return JsonResponse({"error": "Failed to fetch data"}, status=500)

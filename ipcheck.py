
import requests

ABUSEIPDB_KEY = "your_abuseipdb_key"
IPAPI_KEY = "your_ipapi_key"

def get_ip_threat_info(ip):
    try:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
        headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = response.json()["data"]
        return {
            "abuse_score": data["abuseConfidenceScore"],
            "country": data.get("countryCode", "N/A"),
            "full": data
        }
    except Exception as e:
        return {"abuse_score": -1, "country": "N/A", "full": str(e)}

def get_ip_location(ip):
    try:
        url = f"https://ipapi.co/{ip}/json/?key={IPAPI_KEY}"
        response = requests.get(url)
        data = response.json()
        return {
            "lat": data.get("latitude", 0),
            "lon": data.get("longitude", 0),
            "country": data.get("country_name", "Unknown"),
            "full": data
        }
    except Exception as e:
        return {"lat": 0, "lon": 0, "country": "Unknown", "full": str(e)}

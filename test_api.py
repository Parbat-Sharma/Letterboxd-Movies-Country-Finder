import requests

# Timro exact API key
API_KEY = "2744f6eed4729762c8583c1e8a876d83"

def test_tmdb_connection():
    print("Initiating raw API connection test to TMDB...")
    
    # Test parameters: "Inception (2010)"
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": "Inception",
        "year": "2010"
    }
    
    try:
        response = requests.get(url, params=params)
        
        print("\n--- DIAGNOSTIC RESULTS ---")
        print(f"HTTP Status Code : {response.status_code}")
        print(f"Raw JSON Response: {response.text[:300]}...") # Printing first 300 chars
        
        if response.status_code == 401:
            print("\n[CONCLUSION]: 401 Unauthorized. Timro API Key invalid chha wa TMDB le ban gareko chha. Naya account banayera fresh key nikalnu parchha.")
        elif response.status_code == 200 and "results" in response.json():
            if len(response.json()["results"]) == 0:
                print("\n[CONCLUSION]: 200 OK tara list empty chha. TMDB le timro IP block garirako chha wa API parameters match bhayena.")
            else:
                print("\n[CONCLUSION]: API is perfectly working. Problem timro watched.csv ko file formatting ma chha (e.g., BOM characters or hidden spaces in titles).")
        else:
            print("\n[CONCLUSION]: Unexpected error. Check the raw JSON response above.")
            
    except Exception as e:
        print(f"\n[CRITICAL NETWORK FAILURE]: {str(e)}")

if __name__ == "__main__":
    test_tmdb_connection()
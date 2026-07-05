
import csv
import time
import os
import requests
from dotenv import load_dotenv

# Force load the specific api.env file automatically
load_dotenv("api.env")
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json"}

# Hard termination if the key is missing from api.env
if not API_KEY:
    print("[FATAL ERROR] TMDB_API_KEY not found in api.env file.")
    print("Ensure api.env exists and contains: TMDB_API_KEY=your_actual_api_key")
    exit(1)

def get_all_countries():
    """Fetches all valid countries and their ISO codes from TMDB."""
    url = f"{BASE_URL}/configuration/countries"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params, headers=HEADERS).json()
    
    if isinstance(response, dict) and "status_message" in response:
        print(f"\n[API ERROR] {response['status_message']}")
        exit(1)
    
    return {item["english_name"]: item["iso_3166_1"] for item in response}

def get_watched_countries(csv_file):
    """Extracts unique primary countries from watched.csv to build an exclusion list."""
    watched_countries = set()
    
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        movies = list(reader)
        total = len(movies)
        
        print(f"\n[1/3] Analyzing {total} watched movies to build exclusion list...")
        
        for index, row in enumerate(movies, 1):
            title = row.get('Name') or row.get('Title')
            year = row.get('Year')
            if not title:
                continue
                
            print(f"      Processing [{index}/{total}]: {title}".ljust(100), end="\r")
            
            try:
                search = requests.get(f"{BASE_URL}/search/movie", params={
                    "api_key": API_KEY, "query": title, "year": year
                }).json()
                
                if search.get("results"):
                    movie_id = search["results"][0]["id"]
                    details = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY}).json()
                    prod_countries = details.get("production_countries", [])
                    if prod_countries:
                        watched_countries.add(prod_countries[0]["name"])
            except Exception:
                pass
            
            time.sleep(0.2)
            
    print("\n      Exclusion list built successfully.")
    return watched_countries

def get_recommendation_for_country(iso_code):
    """Fetches the highest popularity feature film for a specific country."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_origin_country": iso_code,
        "sort_by": "popularity.desc",
        "vote_count.gte": 10,
        "without_genres": "99"
    }
    
    try:
        response = requests.get(url, params=params).json()
        if response.get("results"):
            movie = response["results"][0]
            year = movie.get('release_date', 'N/A')[:4]
            return f"{movie['title']} ({year})"
        return None
    except Exception:
        return None

def execute_discovery():
    if not os.path.exists("watched.csv"):
        print("[ERROR] watched.csv not found in the current directory.")
        return

    all_countries_map = get_all_countries()
    watched_countries = get_watched_countries("watched.csv")
    
    unwatched_countries = {}
    for country_name, iso_code in all_countries_map.items():
        if country_name not in watched_countries:
            unwatched_countries[country_name] = iso_code

    print(f"\n[2/3] Verified: You have watched movies from {len(watched_countries)} countries.")
    print(f"      Generating watchlist for {len(unwatched_countries)} unexplored countries...\n")

    recommendations = {}
    total_unwatched = len(unwatched_countries)
    
    for index, (country, iso) in enumerate(unwatched_countries.items(), 1):
        print(f"      Fetching recommendation [{index}/{total_unwatched}] for: {country}".ljust(100), end="\r")
        movie = get_recommendation_for_country(iso)
        if movie:
            recommendations[country] = movie
        time.sleep(0.1)

    print("\n\n" + "="*65)
    print("           GLOBAL WATCHLIST: ONE MOVIE PER COUNTRY")
    print("="*65)
    
    for country in sorted(recommendations.keys()):
        print(f"📌 {country.upper()}: {recommendations[country]}")

if __name__ == "__main__":
    execute_discovery()
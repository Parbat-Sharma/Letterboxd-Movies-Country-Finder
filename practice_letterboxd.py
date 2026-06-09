import csv
import time
import os
import requests
from collections import defaultdict, Counter

# Direct Hardcoded API Key (Bypassing .env completely)
API_KEY = "2744f6eed4729762c8583c1e8a876d83"

def fetch_country(title, year):
    base_url = "https://api.themoviedb.org/3"
    try:
        search = requests.get(f"{base_url}/search/movie", params={
            "api_key": API_KEY, "query": title, "year": year
        }).json()

        # Catch actual API errors instead of silently hiding them
        if "status_message" in search:
            print(f"\n[API ERROR] {search['status_message']}")
            return ["API Error"]

        if not search.get("results"):
            return ["Unknown"]

        movie_id = search["results"][0]["id"]
        details = requests.get(f"{base_url}/movie/{movie_id}", params={"api_key": API_KEY}).json()
        
        countries = [c["name"] for c in details.get("production_countries", [])]
        return countries if countries else ["Unknown"]
    except Exception as e:
        return ["Network Error"]

def run_analysis(csv_file):
    country_to_movies = defaultdict(list)
    overall_stats = Counter()
    
    # utf-8-sig removes the hidden Byte Order Mark from Letterboxd CSVs
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        movies = list(reader)
        total = len(movies)
        
        print(f"Starting analysis of {total} movies... Please wait.\n")
        
        for index, row in enumerate(movies, 1):
            title = row.get('Name') or row.get('Title')
            year = row.get('Year')
            
            if not title:
                continue
                
            print(f"[{index}/{total}] Fetching: {title} ({year})...")
            
            countries = fetch_country(title, year)
            
            for c in countries:
                overall_stats[c] += 1
                country_to_movies[c].append(f"{title} ({year})")
            
            time.sleep(0.25)

    # --- FINAL OUTPUT ---
    print("\n" + "="*50)
    print("      GEOGRAPHIC ANALYSIS COMPLETE")
    print("="*50)

    print("\n[1] SUMMARY COUNT:")
    for country, count in overall_stats.most_common():
        print(f"{country}: {count}")

    print("\n[2] DETAILED LIST BY COUNTRY:")
    for country in sorted(country_to_movies.keys()):
        print(f"\n📌 {country.upper()}:")
        for movie in sorted(country_to_movies[country]):
            print(f"   - {movie}")

if __name__ == "__main__":
    FILE = "watched.csv"
    if os.path.exists(FILE):
        run_analysis(FILE)
    else:
        print(f"Error: {FILE} not found! Current directory: {os.getcwd()}")
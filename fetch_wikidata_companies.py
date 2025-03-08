import requests
import pandas as pd

# SPARQL endpoint for Wikidata
WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

# SPARQL query to fetch companies with descriptions
SPARQL_QUERY = """
SELECT ?company ?companyLabel ?industryLabel ?countryLabel ?description WHERE {
  ?company wdt:P31 wd:Q4830453.  # Instance of a company
  OPTIONAL { ?company wdt:P452 ?industry. }
  OPTIONAL { ?company wdt:P17 ?country. }
  OPTIONAL { ?company schema:description ?description. }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 1000
"""

def fetch_wikidata_companies():
    """Fetch company data from Wikidata using SPARQL."""
    headers = {
        "User-Agent": "NER-Entity-Mapper/1.0 (https://github.com/ML-Alchemists-Berlin/NER-Entity-Mapper)",
        "Accept": "application/json"
    }

    response = requests.get(WIKIDATA_SPARQL_URL, params={'query': SPARQL_QUERY, 'format': 'json'}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data["results"]["bindings"]
        
        # Extract relevant fields
        companies = []
        for result in results:
            company = {
                "Company": result["companyLabel"]["value"] if "companyLabel" in result else None,
                "Industry": result["industryLabel"]["value"] if "industryLabel" in result else "Unknown",
                "Country": result["countryLabel"]["value"] if "countryLabel" in result else "Unknown",
                "Description": result["description"]["value"] if "description" in result else "No description available"
            }
            companies.append(company)

        return companies
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

def save_to_csv(data, filename="wikidata_companies.csv"):
    """Save the extracted company data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Fetching company data from Wikidata...")
    companies = fetch_wikidata_companies()

    if companies:
        save_to_csv(companies)
    else:
        print("No data retrieved.")

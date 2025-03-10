from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from difflib import SequenceMatcher

# DBpedia SPARQL Endpoint
DBPEDIA_SPARQL_URL = "http://dbpedia.org/sparql"

def get_best_match(org_name):
    """Fetch the best-matching company entity from DBpedia using SPARQL."""
    
    # SPARQL Query with Dynamic Organization Name
    sparql_query = f"""
    SELECT ?company ?label ?industry ?country ?abstract ?wikiPage WHERE {{
      ?company rdf:type dbo:Company.
      ?company rdfs:label ?label.
      
      OPTIONAL {{ ?company dbo:industry ?industry. }}
      OPTIONAL {{ ?company dbo:country ?country. }}
      OPTIONAL {{ ?company dbo:abstract ?abstract. }}
      OPTIONAL {{ ?company foaf:isPrimaryTopicOf ?wikiPage. }}

      FILTER (CONTAINS(LCASE(?label), LCASE("{org_name}")))
      FILTER (lang(?label) = 'en')
      FILTER (lang(?abstract) = 'en')
    }}
    LIMIT 5
    """

    sparql = SPARQLWrapper(DBPEDIA_SPARQL_URL)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    matches = results["results"]["bindings"]

    if not matches:
        return None

    # Rank results by similarity score
    ranked_matches = sorted(matches, key=lambda x: SequenceMatcher(None, org_name.lower(), x["label"]["value"].lower()).ratio(), reverse=True)

    # Best match
    best_match = ranked_matches[0]

    return {
        "Matched Entity": best_match["label"]["value"],
        "Industry": best_match["industry"]["value"] if "industry" in best_match else "Unknown",
        "Country": best_match["country"]["value"] if "country" in best_match else "Unknown",
        "Description": best_match["abstract"]["value"] if "abstract" in best_match else "No description available",
        "Wikipedia URL": best_match["wikiPage"]["value"] if "wikiPage" in best_match else "No URL available"
    }

if __name__ == "__main__":
    org_name = input("Enter an organization name: ")
    best_match = get_best_match(org_name)

    if best_match:
        print("Best Matching Entity Found:")
        for key, value in best_match.items():
            print(f"{key}: {value}")
    else:
        print("No matching entity found.")

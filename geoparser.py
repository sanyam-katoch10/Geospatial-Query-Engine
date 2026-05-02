

import re
import spacy
from rapidfuzz import process, fuzz
from places_db import ALL_TABLES

nlp = spacy.load("en_core_web_sm")

MATCH_THRESHOLD = 70

STOPWORDS = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "north", "south", "east", "west",
    "the", "which", "what", "how", "show", "give", "compare",
    "graph", "data", "weather", "temperature", "rainfall", "population",
    "area", "highest", "lowest", "average", "entire", "list", "all",
    "following", "month", "year", "city", "cities", "state", "states",
    "country", "countries", "district", "region", "province",
}


def normalize_token(token):
    cleaned = re.sub(r'[-_]+', ' ', token)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned.lower()


def is_stopword(text):
    """Check if a token is a common word (not a place name)."""
    return text.lower().strip() in STOPWORDS


def extract_candidates_nlp(sentence):
    doc = nlp(sentence)
    candidates = []

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "FAC"]:
            candidates.append(ent.text)

    for token in doc:
        if token.pos_ == "PROPN" and token.text.strip():
            already_found = False
            for existing in candidates:
                if token.text.lower() in existing.lower().split():
                    already_found = True
                    break

            if not already_found and token.text not in candidates:
                if not is_stopword(token.text):
                    candidates.append(token.text)

    tokens_list = [t for t in doc if t.pos_ == "PROPN" and t.text.strip()]
    for i in range(len(tokens_list) - 1):
        t1 = tokens_list[i]
        t2 = tokens_list[i + 1]
        if t2.i - t1.i == 1:
            bigram = t1.text + " " + t2.text
            if bigram not in candidates and not is_stopword(bigram):
                candidates.append(bigram)

    seen = set()
    unique = []
    for c in candidates:
        key = c.lower().strip()
        if key and key not in seen and not is_stopword(key):
            seen.add(key)
            unique.append(c)

    final = []
    for candidate in unique:
        is_part_of_bigger = False
        for other in unique:
            if candidate != other:
                other_words = other.lower().split()
                if len(other_words) > 1 and candidate.lower() in other_words:
                    is_part_of_bigger = True
                    break
        if not is_part_of_bigger:
            final.append(candidate)

    return final


def fuzzy_match_token(token):
    normalized = normalize_token(token)

    best_match = None
    best_score = 0
    best_table = None
    best_coords = None

    for table_name, place_dict in ALL_TABLES.items():
        place_names = list(place_dict.keys())

        result = process.extractOne(
            normalized,                  
            place_names,                 
            scorer=fuzz.WRatio,          
            score_cutoff=MATCH_THRESHOLD 
        )

        if result and result[1] > best_score:
            best_match = result[0]
            best_score = result[1]
            best_table = table_name
            best_coords = place_dict[best_match]

    if best_match:
        return {
            "token": token,              
            "canonical_name": best_match, 
            "table": best_table,          
            "confidence": round(best_score, 1),
            "latitude": round(best_coords[0], 4),
            "longitude": round(best_coords[1], 4)
        }

    return None


def parse_geonames(sentence):
    candidates = extract_candidates_nlp(sentence)


    results = []
    seen = set()
    for candidate in candidates:
        match = fuzzy_match_token(candidate)
        if match and match["canonical_name"] not in seen:
            results.append(match)
            seen.add(match["canonical_name"])

    if not results:
       
        words = re.findall(r'\b\w+\b', sentence)
        for word in words:
            if len(word) < 3: continue
            match = fuzzy_match_token(word)
            if match and match["confidence"] >= 85 and match["canonical_name"] not in seen:
                results.append(match)
                seen.add(match["canonical_name"])

    return results


if __name__ == "__main__":
    test_sentences = [
        "Which of the following saw the highest average temperature in January, Maharashtra, Ahmedabad or entire New-Zealand?",
        "Show me a graph of rainfall for Chennai for the month of October",
        "Compare population of Indya and Austrla",
        "What is the area of Rajasthan and Gujrat?",
        "Give me weather data for New York and Londan",
        "List all cities in Uttar Pradesh",
        "Compare Shimla and Gangtok weather",
        "Show temperature of California and Tokyo",
        "What is the rainfall in Mumbai and Delhi?",
        "Compare the area of Maharashtra and Gujarat",
        "Which city has higher population: Chennai or Bangalore?",
        "Show me temperature trends for New Zealand and Australia",
        "How much rain fell in Kolkata last month?",
        "Compare population density of Tokyo and New York",
        "Find the highest temperature recorded in Uttar Pradesh",
        "Give rainfall data for Kerala and Tamil Nadu",
        "Which state has larger area: Rajasthan or Madhya Pradesh?",
        "Compare population growth in Mumbai and Delhi over 5 years",
        "What is the average rainfall in Karnataka?"
    ]

    print("=" * 80)
    print("GEOSPATIAL ENTITY PARSER - TEST RESULTS")
    print("=" * 80)

    for idx, sentence in enumerate(test_sentences, 1):
        print(f"\n[Test {idx}]")
        print(f"Input: {sentence}")
        print("-" * 60)

        results = parse_geonames(sentence)

        if results:
            for r in results:
                print(f"  {r['token']:20} -> {r['canonical_name']:20} "
                      f"[{r['table']:7}]  {r['confidence']}%")
        else:
            print("  No place names found")

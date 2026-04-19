import spacy
from rapidfuzz import process, fuzz
from places_db import ALL_TABLES

nlp = spacy.load("en_core_web_sm")

MATCH_THRESHOLD = 72


def extract_candidates_nlp(sentence):
    doc = nlp(sentence)

    candidates = []

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            candidates.append(ent.text)

    # fallback for capitalized words spaCy missed
    for token in doc:
        if token.text[0].isupper() and token.text.isalpha():
            if token.text not in candidates:
                candidates.append(token.text)

    # remove duplicates
    seen = set()
    unique = []

    for c in candidates:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)

    return unique


def fuzzy_match_token(token):
    best_match = None
    best_score = 0
    best_table = None

    for table_name, place_list in ALL_TABLES.items():
        result = process.extractOne(
            token.lower(),
            place_list,
            scorer=fuzz.WRatio,
            score_cutoff=MATCH_THRESHOLD
        )

        if result and result[1] > best_score:
            best_match = result[0]
            best_score = result[1]
            best_table = table_name

    if best_match:
        return {
            "token": token,
            "canonical_name": best_match,
            "table": best_table,
            "confidence": round(best_score, 1)
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

    return results

if __name__ == "__main__":
    test_sentences = [
        "Which of the following saw the highest average temperature in January, Maharashtra, Ahmedabad or entire New Zealand?",
        "Show me a graph of rainfall for Chennai for the month of October",
        "Compare population of Indya and AUSttrlya",      
        "What is the area of Rajasthan and Gujrat?",    
        "Give me weather data for New York and Londan",  
    ]

    for sentence in test_sentences:
        print(f"\nInput: {sentence}")
        results = parse_geonames(sentence)
        if results:
            for r in results:
                print(f"  Token: {r['token']:15} → canonical: {r['canonical_name']:20} table: {r['table']:8} confidence: {r['confidence']}%")
        else:
            print("  No place names found")

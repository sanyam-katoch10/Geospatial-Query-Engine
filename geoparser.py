import nltk
from rapidfuzz import process, fuzz
from places_db import ALL_TABLES

MATCH_THRESHOLD = 72


def extract_candidates_nlp(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)
    ne_tree = nltk.ne_chunk(pos_tags, binary=False)
    candidates = []
    for subtree in ne_tree:
        if isinstance(subtree, nltk.Tree):
            entity_type = subtree.label()
           
            if entity_type in ("GPE", "LOCATION", "FACILITY"):
           
                entity_text = " ".join(word for word, tag in subtree.leaves())
                candidates.append(entity_text)

    import re
    for token in tokens:
        if re.match(r'^[A-Z][a-zA-Z\-]{2,}$', token):
            if token not in candidates and token.lower() not in {"The", "A", "An", "In", "On", "At",
                "Which", "What", "Show", "Give", "Find", "Compare", "List", "January", "February",
                "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"}:
                candidates.append(token)

   
    seen = set()
    unique = []
    for c in candidates:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)

    return unique


def fuzzy_match_token(token):
    """
    Fuzzy match a token against all canonical place tables.
    RapidFuzz's WRatio handles:
    - spelling errors (Gujrat → Gujarat)
    - different spellings (New-Zealand → new zealand)
    - partial matches
    """
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
    """
    Main pipeline:
    sentence → NLTK NE extraction → fuzzy canonical matching → results
    """
    candidates = extract_candidates_nlp(sentence)
    results = []
    seen_canonicals = set()

    for candidate in candidates:
        match = fuzzy_match_token(candidate)
        if match and match["canonical_name"] not in seen_canonicals:
            results.append(match)
            seen_canonicals.add(match["canonical_name"])

    return results


if __name__ == "__main__":
    test_sentences = [
        "Which of the following saw the highest average temperature in January, Maharashtra, Ahmedabad or entire New Zealand?",
        "Show me a graph of rainfall for Chennai for the month of October",
        "Compare population of Indya and Pakstan",      
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

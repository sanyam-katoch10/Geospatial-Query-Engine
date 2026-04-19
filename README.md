# Place Name Identifier

## Setup
```bash
pip install -r requirements.txt

python -c "
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
"
```

## Run
```bash
python app.py
# open http://localhost:5000
```

## Test core logic directly
```bash
python geoparser.py
```

## How it works
1. NLTK ne_chunk() → Named Entity Recognition (finds GPE, LOCATION entities)
2. Capitalized word fallback → catches anything NER missed
3. RapidFuzz WRatio → fuzzy matches to canonical tables, handles typos

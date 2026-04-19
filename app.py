from flask import Flask, request, jsonify, render_template
from geoparser import parse_geonames

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json()
    sentence = data.get("sentence", "").strip()

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    results = parse_geonames(sentence)
    return jsonify({
        "sentence": sentence,
        "results": results,
        "count": len(results)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

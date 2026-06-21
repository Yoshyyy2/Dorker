from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "a5e2e510ef7f9f54f345ac61fc7e534dde05b525a8d4c8795f665f88981dc904"

def search_serpapi(dork, num_results=50):
    url = "https://serpapi.com/search.json"
    params = {
        "q": dork,
        "api_key": API_KEY,
        "num": num_results,
        "engine": "google"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        results = []
        if "organic_results" in data:
            for item in data.get("organic_results", []):
                results.append({
                    "link": item.get("link", "")
                })
        return results
    except:
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    dork = data.get("dork", "")
    num = int(data.get("num", 50))

    if not dork:
        return jsonify({"error": "No dork provided"}), 400

    results = search_serpapi(dork, num)
    return jsonify({"results": results})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

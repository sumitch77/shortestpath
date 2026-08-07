"""
Web server for the Miniature Navigation System.
Serves the frontend and exposes a JSON API for route finding.
"""

from flask import Flask, jsonify, render_template, request

from navigation import CITIES, shortest_route

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", cities=sorted(CITIES.keys()))


@app.route("/api/cities")
def get_cities():
    """Return the list of available cities."""
    return jsonify({"cities": sorted(CITIES.keys())})


@app.route("/api/route", methods=["POST"])
def get_route():
    """Find the shortest route between two cities."""
    data = request.get_json(silent=True) or {}
    source = (data.get("source") or "").strip()
    destination = (data.get("destination") or "").strip()

    if source not in CITIES:
        return jsonify({"error": f"'{source}' is not a valid city."}), 400
    if destination not in CITIES:
        return jsonify({"error": f"'{destination}' is not a valid city."}), 400
    if source == destination:
        return jsonify({"error": "Source and destination must be different."}), 400

    route, distance = shortest_route(source, destination)

    if not route:
        return jsonify({"error": f"No route found between {source} and {destination}."}), 404

    return jsonify(
        {
            "route": route,
            "distance": round(distance, 2),
            "source": source,
            "destination": destination,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

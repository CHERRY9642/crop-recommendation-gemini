from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

API_KEY = "AIzaSyAH7aYrAZsTEf-XA9fz3crl0kRDl5hcmCQ"  # Replace with your Gemini API key
MODEL_NAME = "gemini-2.5-pro"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    try:
        district = data.get('district', 'Unknown')
        state = data.get('state', 'Unknown')
        country = data.get('country', 'Unknown')
        nitrogen = data.get('nitrogen', 'Unknown')
        phosphorus = data.get('phosphorus', 'Unknown')
        potassium = data.get('potassium', 'Unknown')
        ph = data.get('ph', 'Unknown')
        growing_season = data.get('growingSeason', 'Unknown')
        temperature = data.get('temperature', 'Unknown')
        humidity = data.get('humidity', 'Unknown')
        wind_speed = data.get('windSpeed', 'Unknown')
        cloudiness = data.get('cloudiness', 'Unknown')
        water_availability = data.get('waterAvailability', 'Unknown')
        crop_history = data.get('cropHistory', '')

        prompt = f"""
You are an expert agronomist. Based on the following soil and environmental data, provide 2 or 3 crop recommendations best suited for the farm. For each crop provide the crop name, suitability percentage match, brief reason, expected yield, duration, and basic cultivation requirements.

Farm details:
- Location: {district}, {state}, {country}
- Growing Season: {growing_season}
- Soil Nutrients (N, P, K in %): N={nitrogen}, P={phosphorus}, K={potassium}
- Soil pH: {ph}
- Weather Conditions: Temperature={temperature}°C, Humidity={humidity}%, Wind Speed={wind_speed} km/h, Cloudiness={cloudiness}
- Water Availability: {water_availability}
- Crop History: {crop_history}

Recommend crops that optimize yield and soil health for these conditions. Format the answer exactly as:

Crop Recommendations
Crop Name
XX% Match
Reason
Expected Yield:
Duration:
Requirements:
"""

        body = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(ENDPOINT, headers=headers, json=body)
        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        resp_json = response.json()
        text = resp_json['candidates'][0]['content']['parts'][0]['text']

        match = re.search(r"Crop Recommendations(.+?)(\n\n|$)", text, re.DOTALL)
        recommendation = match.group(1).strip() if match else text

        return jsonify({"recommendation": recommendation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

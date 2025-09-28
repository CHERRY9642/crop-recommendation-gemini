from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

API_KEY = "AIzaSyAH7aYrAZsTEf-XA9fz3crl0kRDl5hcmCQ"  # Replace with your actual Gemini API key
MODEL_NAME = "gemini-2.5-pro"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    try:
        # Build prompt text
        prompt = f"""
Based on the following farm data, recommend only 2 or 3 suitable crops with the crop name, match percentage, a short reason why it's suitable, expected yield, duration, and basic requirements. Format the response as a list like this:

Crop Recommendations
Tomato
95% Match
Excellent choice for your soil conditions and climate
Expected Yield:
4-6 kg per plant
Duration:
70-80 days
Requirements:
Well-drained soil
6-8 hours sunlight
Regular watering

Location: {data['district']}, {data['state']}, {data['country']}
Soil Nutrients: N={data['nitrogen']}, P={data['phosphorus']}, K={data['potassium']}
Soil pH: {data['ph']}
Temperature: {data['temperature']}
Humidity: {data['humidity']}
Rainfall: {data['rainfall']}
Water Availability: {data['waterAvailability']}
Crop History: {data.get('cropHistory', '')}
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

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(ENDPOINT, headers=headers, json=body)
        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        resp_json = response.json()
        text = resp_json['candidates'][0]['content']['parts'][0]['text']

        # Extract crop recommendations section if present
        match = re.search(r"Crop Recommendations(.+?)(\n\n|$)", text, re.DOTALL)
        recommendation = match.group(1).strip() if match else text

        return jsonify({"recommendation": recommendation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

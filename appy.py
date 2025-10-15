import os
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENAPI = {
  "openapi": "3.0.0",
  "info": {"title": "KFT CMA Lite API", "version": "1.0"},
  "paths": {
    "/cma": {
      "post": {
        "summary": "Create a CMA",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "subject": {
                    "type": "object",
                    "properties": {
                      "address": {"type": "string"},
                      "beds": {"type": "integer"},
                      "baths": {"type": "number"},
                      "gla_sqft": {"type": "integer"}
                    },
                    "required": ["address","beds","baths","gla_sqft"]
                  }
                },
                "required": ["subject"]
              }
            }
          }
        },
        "responses": {"200": {"description": "CMA results"}}
      }
    }
  }
}

@app.route("/openapi.json", methods=["GET"])
def openapi():
    return jsonify(OPENAPI)

@app.route("/cma", methods=["POST"])
def cma():
    body = request.get_json(force=True) or {}
    subject = body.get("subject", {})
    # ---- fake CMA so you can test end-to-end now
    return jsonify({
        "subject": subject,
        "comps": [
          {
            "address": "123 Test St",
            "status": "Sold",
            "price": 500000,
            "gla_sqft": 2400,
            "distance_mi": 0.3,
            "adjustments": [
              {"factor":"GLA","amount":-10000,"note":"Comp larger by ~80 sf @ $125/sf"}
            ],
            "net_adjusted_price": 490000,
            "weight": 0.8
          }
        ],
        "valuation": {
          "low": 480000,
          "likely": 495000,
          "high": 510000,
          "confidence": 0.8,
          "recommended_list_price": 499000,
          "notes": "Tight comps; prices up ~3% in last 6 months."
        },
        "disclaimers": [
          "Prepared as a Comparative Market Analysis by a real estate licensee. Not an appraisal."
        ]
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))  # Render assigns $PORT
    app.run(host="0.0.0.0", port=port)

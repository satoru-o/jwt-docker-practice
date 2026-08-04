import os
from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)

with open("public.pem", "rb") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = "RS256"


@app.get("/health")
def health():
    return jsonify({"status": "ok", "role": "verifier-only"})

@app.post("/verify")
def verify():
    data = request.get_json(silent=True) or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "token is required"}), 400
    
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"invalid token: {e}"}), 401
    
    return jsonify({"valid": True, "claims": payload})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
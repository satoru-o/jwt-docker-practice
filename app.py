import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 5  # 5分(動作確認しやすいように短め)

# デモ用のダミーユーザーDB(本番なら当然ハッシュ化 + 本物のDBを使う)
USERS = {
    "alice": "wonderland",
}


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) != password:
        return jsonify({"error": "invalid credentials"}), 401

    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jsonify({"access_token": token, "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS})


@app.get("/protected")
def protected():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "missing bearer token"}), 401

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"invalid token: {e}"}), 401

    return jsonify({"message": f"hello {payload['sub']}, this is protected data", "claims": payload})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
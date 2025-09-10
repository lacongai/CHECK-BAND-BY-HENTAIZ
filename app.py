"""
Updated Flask API for use with:
- Telegram bot webhooks
- Discord bot webhooks
- Website calls
- Termux (local execution)

Features & improvements:
- Use environment variable API_KEY or multiple keys
- Accept key as query param, form param or Authorization header
- Cleaner error handling & logging
- CORS enabled for browser use
- Dedicated webhook endpoints for Telegram and Discord (simple verification via secret)
- Robust file/token parsing (supports ZIP uploads)
- JWT decoding without signature verification (safe for inspection only)
- Proxy decode endpoint preserved but improved
- Helpful /help endpoint

Save as api_updated.py and run: python api_updated.py
"""

from flask import Flask, request, jsonify, abort, Response
from flask_cors import CORS
import os
import requests
import json
import re
import datetime
import jwt  # pyjwt
import tempfile
import zipfile
import logging
from typing import List, Dict, Any, Optional

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# API keys: either a single key (HARD_FALLBACK) or comma-separated keys in env var
API_KEYS = [k.strip() for k in os.environ.get("API_KEYS", "hentaiz").split(",") if k.strip()]
# Optional secrets for Telegram/Discord webhook verification
TELEGRAM_SECRET = os.environ.get("TELEGRAM_SECRET")
DISCORD_SECRET = os.environ.get("DISCORD_SECRET")

# ==============================
# Helpers
# ==============================

def check_key(provided: Optional[str]) -> bool:
    """Accept key provided via query param, form, or Authorization header."""
    if not provided:
        return False
    # allow either plain key or Bearer <key>
    if provided.lower().startswith("bearer "):
        provided = provided[7:].strip()
    return provided in API_KEYS


def get_key_from_request() -> Optional[str]:
    # 1. Authorization header
    auth = request.headers.get("Authorization")
    if auth:
        return auth
    # 2. query param or form param
    return request.args.get("key") or request.form.get("key")


def parse_token_file_upload(file_storage) -> List[str]:
    """Extract tokens from uploaded file (txt/json or zip containing such files)"""
    tokens: List[str] = []
    if not file_storage:
        return tokens
    tmp_path = os.path.join(tempfile.gettempdir(), file_storage.filename)
    file_storage.save(tmp_path)
    try:
        if tmp_path.lower().endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as z:
                extract_dir = tempfile.mkdtemp()
                z.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.lower().endswith((".txt", ".json")):
                            p = os.path.join(root, fn)
                            tokens.extend(extract_tokens_from_text_file(p))
        else:
            tokens.extend(extract_tokens_from_text_file(tmp_path))
    except Exception as e:
        logger.warning("parse_token_file_upload error: %s", e)
    return list(dict.fromkeys(tokens))  # unique


def extract_tokens_from_text_file(path: str) -> List[str]:
    tokens: List[str] = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip().strip('"')
                if len(line) > 20:
                    tokens.append(line)
    except Exception as e:
        logger.warning("extract_tokens_from_text_file(%s) error: %s", path, e)
    return tokens


def decode_jwt_without_verification(token: str) -> Dict[str, Any]:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        exp_ts = decoded.get("exp")
        exp_time = None
        expired = None
        if exp_ts:
            exp_time = datetime.datetime.utcfromtimestamp(exp_ts).strftime("%Y-%m-%d %H:%M:%S UTC")
            expired = datetime.datetime.utcfromtimestamp(exp_ts) < datetime.datetime.utcnow()
        return {"ok": True, "payload": decoded, "exp_time": exp_time, "expired": expired}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ==============================
# Basic routes
# ==============================

@app.route("/", methods=["GET"]) 
def home():
    return jsonify({"status": "ok", "message": "API running", "time": datetime.datetime.utcnow().isoformat() + "Z"})


@app.route("/help", methods=["GET"]) 
def help_endpoint():
    base = request.url_root.rstrip("/")
    commands = {
        f"{base}/api/check?key=<KEY>&uid=<UID>": "Check account ban status",
        f"{base}/api/decode?key=<KEY>&token=<TOKEN>": "Decode token via proxy",
        f"{base}/api/check_token_file?key=<KEY>": "Upload file or token_file param to decode tokens",
        f"{base}/webhook/telegram?key=<KEY>": "Telegram webhook receiver (POST)",
        f"{base}/webhook/discord?key=<KEY>": "Discord webhook receiver (POST)",
    }
    return jsonify({"status": "ok", "commands": commands})

# ==============================
# Example: check ban (Free Fire) - returns JSON dict (no flask jsonify inside helper)
# ==============================

def get_player_info(player_id: str) -> Dict[str, str]:
    # Keep original behaviour but resilient to errors
    try:
        cookies = {"region": "MA", "language": "ar", "session_key": "efwfzwesi9ui8drux4pmqix4cosane0y"}
        headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Origin": "https://shop2game.com",
            "Referer": "https://shop2game.com/app/100067/idlogin",
            "User-Agent": "Mozilla/5.0",
            "accept": "application/json",
            "content-type": "application/json",
        }
        json_data = {"app_id": 100067, "login_id": f"{player_id}", "app_server_id": 0}
        res = requests.post("https://shop2game.com/api/auth/player_id_login", cookies=cookies, headers=headers, json=json_data, timeout=6)
        if res.status_code == 200:
            data = res.json()
            return {"nickname": data.get("nickname", "❌ Không rõ"), "region": data.get("region", "❌ Không rõ")}
    except Exception as e:
        logger.debug("get_player_info error: %s", e)
    return {"nickname": "❌ Không thể lấy tên", "region": "❌ Không thấy khu vực"}


def check_banned_dict(player_id: str) -> Dict[str, Any]:
    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=6)
        player_info = get_player_info(player_id)
        if response.status_code == 200:
            data = response.json().get("data", {})
            is_banned = data.get("is_banned", 0)
            period = data.get("period", 0)
            duration = f"{period} ngày" if is_banned and period > 0 else ("Khoá vĩnh viễn" if is_banned else "Không bị khóa")
            return {
                "status": "success",
                "uid": player_id,
                "nickname": player_info.get("nickname"),
                "region": player_info.get("region"),
                "banned": bool(is_banned),
                "duration": duration,
                "raw_data": data,
            }
        return {"status": "error", "message": "Không thể lấy trạng thái cấm từ máy chủ Garena", "http_status": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/api/check", methods=["GET"]) 
def api_check():
    provided = get_key_from_request()
    if not check_key(provided):
        return jsonify({"error": "Unauthorized. Invalid key"}), 403
    player_id = request.args.get("uid")
    if not player_id:
        return jsonify({"error": "uid parameter required"}), 400
    result = check_banned_dict(player_id)
    status_code = 200 if result.get("status") == "success" else 500
    return jsonify(result), status_code

# ==============================
# Decode token(s) from uploaded file or param
# ==============================

@app.route("/api/check_token_file", methods=["GET", "POST"]) 
def api_check_token_file():
    provided = get_key_from_request()
    if not check_key(provided):
        return jsonify({"error": "Unauthorized. Invalid key"}), 403

    # tokens can be provided via: file upload, token_file param (comma-separated), or token param
    uploaded = request.files.get("file")
    token_param = request.args.get("token_file") or request.form.get("token_file") or request.args.get("token") or request.form.get("token")

    tokens: List[str] = []
    if uploaded:
        tokens = parse_token_file_upload(uploaded)
    elif token_param:
        tokens = [t.strip().strip('"') for t in token_param.split(",") if len(t.strip()) > 20]
    else:
        return jsonify({"error": "token_file parameter or file upload required"}), 400

    results = []
    for idx, token in enumerate(tokens, start=1):
        decoded = decode_jwt_without_verification(token)
        if decoded.get("ok"):
            results.append({"index": idx, "status": "success", "token": token, "payload": decoded.get("payload"), "exp": decoded.get("exp_time"), "expired": decoded.get("expired")})
        else:
            results.append({"index": idx, "status": "error", "token": token, "error": decoded.get("error")})
    return jsonify({"count": len(results), "results": results})

# ==============================
# Proxy decode (preserve existing proxy behaviour, but safer)
# ==============================

@app.route("/api/decode", methods=["GET", "POST"]) 
def api_decode_proxy():
    provided = get_key_from_request()
    if not check_key(provided):
        return jsonify({"error": "Unauthorized. Invalid key"}), 403

    token = request.args.get("token") or request.form.get("token")
    uploaded = request.files.get("file")
    tokens: List[str] = []
    if uploaded:
        tokens = parse_token_file_upload(uploaded)
    elif token:
        tokens = [t.strip().strip('"') for t in token.split(",") if len(t.strip()) > 20]
    else:
        return jsonify({"error": "token parameter or file upload required"}), 400

    results = []
    for idx, tk in enumerate(tokens, start=1):
        try:
            # Proxy to existing vercel service but with timeout and error handling
            url = f"https://check-token-nbau.vercel.app/api/check_token_file?key={API_KEYS[0]}&token_file={tk}"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                results.append({"index": idx, "status": "success", "raw": resp.json()})
            else:
                results.append({"index": idx, "status": "error", "message": f"HTTP {resp.status_code}"})
        except Exception as e:
            results.append({"index": idx, "status": "error", "message": str(e)})
    return jsonify({"count": len(results), "results": results})

# ==============================
# Guest accounts scanner
# ==============================

@app.route("/api/guest_accounts", methods=["GET", "POST"]) 
def api_guest_accounts():
    provided = get_key_from_request()
    if not check_key(provided):
        return jsonify({"error": "Unauthorized. Invalid key"}), 403

    file_param = request.args.get("file") or request.form.get("file")
    dir_param = request.args.get("dir", ".")
    uploaded = request.files.get("file")

    output_data = []
    paths_to_scan: List[str] = []

    if uploaded:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded.filename)
        uploaded.save(tmp_path)
        if tmp_path.lower().endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as z:
                extract_dir = tempfile.mkdtemp()
                z.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.lower().endswith((".json", ".dat", ".txt")):
                            paths_to_scan.append(os.path.join(root, fn))
        else:
            paths_to_scan.append(tmp_path)
    elif file_param and os.path.exists(file_param):
        paths_to_scan.append(file_param)
    else:
        # scan directory
        if not os.path.exists(dir_param):
            return jsonify({"error": f"Directory not found: {dir_param}"}), 404
        for fn in os.listdir(dir_param):
            if fn.lower().endswith((".dat", ".json", ".txt")):
                paths_to_scan.append(os.path.join(dir_param, fn))

    for path in paths_to_scan:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            try:
                js = json.loads(content)
                guest_info = js.get("guest_account_info", {}) or js
                uid = guest_info.get("com.garena.msdk.guest_uid")
                password = guest_info.get("com.garena.msdk.guest_password")
                if uid and password:
                    output_data.append({"file": path, "uid": str(uid).strip('"'), "password": str(password).strip('"')})
            except Exception:
                matches = re.findall(r'uid["\']?\s*[:=]\s*["\']?(\d+)["\']?.*?password["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)', content, re.I)
                for u, p in matches:
                    output_data.append({"file": path, "uid": u, "password": p})
        except Exception as e:
            logger.warning("Error reading %s: %s", path, e)

    return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})

# ==============================
# Token generation via external service (kept as simple wrapper)
# ==============================

@app.route("/api/token", methods=["GET", "POST"]) 
def api_token_generate():
    provided = get_key_from_request()
    if not check_key(provided):
        return jsonify({"error": "Unauthorized. Invalid key"}), 403

    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("password") or request.form.get("password")
    file_param = request.args.get("file") or request.form.get("file")
    uploaded = request.files.get("file")

    API_URL = os.environ.get("EXTERNAL_TOKEN_API", "http://narayan-gwt-token.vercel.app/token?uid={}&password={}")
    output_data = []

    def fetch_token(u: str, p: str) -> Dict[str, Optional[str]]:
        try:
            url = API_URL.format(u, p)
            res = requests.get(url, timeout=6)
            if res.status_code == 200:
                token = res.json().get("token")
                return {"uid": u, "token": token}
        except Exception as e:
            logger.warning("fetch_token error for %s: %s", u, e)
        return {"uid": u, "token": None}

    if uid and password:
        res = fetch_token(uid.strip('"'), password.strip('"'))
        if res["token"]:
            output_data.append(res)
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})

    paths_to_scan: List[str] = []
    if uploaded:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded.filename)
        uploaded.save(tmp_path)
        paths_to_scan.append(tmp_path)
        if tmp_path.lower().endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as z:
                extract_dir = tempfile.mkdtemp()
                z.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.lower().endswith((".json", ".dat", ".txt")):
                            paths_to_scan.append(os.path.join(root, fn))
    elif file_param and os.path.exists(file_param):
        paths_to_scan.append(file_param)

    for path in paths_to_scan:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            pairs = re.findall(r'uid["\']?\s*[:=]\s*["\']?(\d+)["\']?.*?password["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)["\']?', content, re.I)
            for u, p in pairs:
                result = fetch_token(u, p)
                if result["token"]:
                    output_data.append(result)
        except Exception as e:
            logger.warning("Error reading %s: %s", path, e)

    if output_data:
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})
    return jsonify({"error": "No valid uid/password found"}), 404

# ==============================
# Simple webhook endpoints for Telegram & Discord
# - These are generic receivers. Put your bot logic here or forward
# - Verification: optional secret in header X-Webhook-Token or in query param
# ==============================

@app.route("/webhook/telegram", methods=["POST"]) 
def webhook_telegram():
    # verify
    provided = request.headers.get("X-Webhook-Token") or request.args.get("token")
    if TELEGRAM_SECRET and provided != TELEGRAM_SECRET:
        return jsonify({"error": "Invalid webhook token"}), 403
    payload = request.get_json(silent=True) or {}
    # Example: forward to your bot processing function or write to file
    logger.info("Telegram webhook received: %s", json.dumps(payload)[:400])
    # Respond quickly for webhook
    return jsonify({"status": "received", "service": "telegram"})


@app.route("/webhook/discord", methods=["POST"]) 
def webhook_discord():
    provided = request.headers.get("X-Webhook-Token") or request.args.get("token")
    if DISCORD_SECRET and provided != DISCORD_SECRET:
        return jsonify({"error": "Invalid webhook token"}), 403
    payload = request.get_json(silent=True) or {}
    logger.info("Discord webhook received: %s", json.dumps(payload)[:400])
    return jsonify({"status": "received", "service": "discord"})

# ==============================
# Run
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5055))
    host = os.environ.get("HOST", "0.0.0.0")
    logger.info("Starting API on %s:%s", host, port)
    app.run(host=host, port=port, debug=False)

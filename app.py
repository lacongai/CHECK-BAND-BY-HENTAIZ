from flask import Flask, request, jsonify, Response
import requests
import json
import os
import re
import datetime
import jwt  # pyjwt

app = Flask(__name__)

API_KEY = "hentaiz"  # 🔑 key cố định

# ==============================
# Trang chủ
# ==============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ API Check Token Account đang chạy!"
    })

# ==============================
# Hàm lấy tên + khu vực
# ==============================
def get_player_info(player_id):
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
    try:
        res = requests.post("https://shop2game.com/api/auth/player_id_login",
                            cookies=cookies, headers=headers, json=json_data)
        if res.status_code == 200:
            data = res.json()
            return {
                "nickname": data.get("nickname", "❌ Không rõ"),
                "region": data.get("region", "❌ Không rõ")
            }
    except:
        pass
    return {"nickname": "❌ Không thể lấy tên", "region": "❌ Không thấy khu vực"}

# ==============================
# Check ban
# ==============================
def check_banned(player_id):
    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        player_info = get_player_info(player_id)
        if response.status_code == 200:
            data = response.json().get("data", {})
            is_banned = data.get("is_banned", 0)
            period = data.get("period", 0)
            duration = f"{period} ngày" if is_banned and period > 0 else ("Khoá vĩnh viễn" if is_banned else "Không bị khóa")
            result = {
                "✅ status": "Kiểm tra thành công",
                "🆔 UID": player_id,
                "🏷️ Nickname": player_info["nickname"],
                "🌍 Region": player_info["region"],
                "🔒 Account": "🚫 BỊ KHOÁ" if is_banned else "✅ BÌNH THƯỜNG",
                "⏳ Duration": duration,
                "📊 Banned?": bool(is_banned),
                "💎 Powered by": "t.me/@henntaiiz",
            }
            return jsonify(result)
        return jsonify({"❌ lỗi": "Không thể lấy trạng thái cấm từ máy chủ Garena"}), 500
    except Exception as e:
        return jsonify({"💥 exception": str(e)}), 500

@app.route("/api/check", methods=["GET"])
def api_check():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403
    player_id = request.args.get("uid")
    if not player_id:
        return jsonify({"error": "⚠️ Cần phải có ID người chơi (uid)!"}), 400
    return check_banned(player_id)

# ==============================
# Decode token trực tiếp
# ==============================
@app.route("/api/check_token_file", methods=["GET"])
def check_token_file():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403
    token_file = request.args.get("token_file")
    if not token_file:
        return jsonify({"error": "❌ token_file parameter is required"}), 400

    tokens = token_file.split(",")
    results = []
    for idx, token in enumerate(tokens, start=1):
        token = token.strip()
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp_ts = decoded.get("exp")
            exp_time, expired, message = None, None, "Không có thời gian hết hạn"
            if exp_ts:
                exp_time = datetime.datetime.fromtimestamp(exp_ts)
                expired = exp_time < datetime.datetime.utcnow()
                message = f"Token expired at {exp_time}" if expired else f"Token valid until {exp_time}"
            results.append({
                "index": idx, "status": "success", "message": message,
                "decode_message": "✅ Token decode thành công",
                "expired": expired,
                "exp_time": exp_time.strftime("%Y-%m-%d %H:%M:%S") if exp_time else None,
                "payload": decoded, "token": token
            })
        except Exception as e:
            results.append({"index": idx, "status": "error", "message": f"❌ Decode lỗi: {str(e)}",
                            "decode_message": "❌ Token decode thất bại", "expired": None, "exp_time": None,
                            "payload": None, "token": token})
    return jsonify({"results": results})

# ==============================
# Decode token qua proxy
# ==============================
@app.route("/api/decode", methods=["GET"])
def api_decode_proxy():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "❌ token parameter is required"}), 400
    try:
        url = f"https://check-token-nbau.vercel.app/api/check_token_file?key={API_KEY}&token_file={token}"
        response = requests.get(url, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"results": [{"index": 1, "status": "error", "message": f"❌ Exception: {str(e)}"}]}), 500

# ==============================
# Guest Accounts
# ==============================
@app.route("/api/guest_accounts", methods=["GET"])
def api_guest_accounts():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403
    file_param = request.args.get("file")
    dir_param = request.args.get("dir", ".")
    output_data = []
    if file_param:
        if not os.path.exists(file_param):
            return jsonify({"error": f"❌ File not found: {file_param}"}), 404
        try:
            with open(file_param, "r", encoding="utf-8") as f:
                content = json.load(f)
            guest_info = content.get("guest_account_info", {})
            uid = guest_info.get("com.garena.msdk.guest_uid", "").strip()
            password = guest_info.get("com.garena.msdk.guest_password", "").strip()
            if uid and password:
                output_data.append({"file": file_param, "uid": uid, "password": password})
        except Exception as e:
            return jsonify({"error": f"❌ Error reading file {file_param}: {e}"}), 500
    else:
        if not os.path.exists(dir_param):
            return jsonify({"error": f"❌ Directory not found: {dir_param}"}), 404
        dat_files = [f for f in os.listdir(dir_param) if f.endswith(".dat")]
        if not dat_files:
            return jsonify({"error": "❌ No .dat files found in directory"}), 404
        for dat_file in dat_files:
            try:
                with open(os.path.join(dir_param, dat_file), "r", encoding="utf-8") as f:
                    content = json.load(f)
                guest_info = content.get("guest_account_info", {})
                uid = guest_info.get("com.garena.msdk.guest_uid", "").strip()
                password = guest_info.get("com.garena.msdk.guest_password", "").strip()
                if uid and password:
                    output_data.append({"file": dat_file, "uid": uid, "password": password})
            except Exception as e:
                print(f"⚠️ Error reading {dat_file}: {e}")
    output_file = os.path.join(dir_param, "ind_ind.json")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, indent=4, ensure_ascii=False)
    return jsonify({"status": "success", "count": len(output_data), "output_file": output_file, "accounts": output_data})

# ==============================
# Generate token từ uid/pass
# ==============================
@app.route("/api/token", methods=["GET"])
def api_token_generate():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403
    uid = request.args.get("uid")
    password = request.args.get("password")
    file_param = request.args.get("file")
    API_URL = "http://narayan-gwt-token.vercel.app/token?uid={}&password={}"
    output_data = []

    def fetch_token(uid, password):
        try:
            url = API_URL.format(uid, password)
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                token = res.json().get("token")
                if token:
                    return {"uid": uid, "token": token}
        except Exception as e:
            print(f"⚠️ Error fetching token for {uid}: {e}")
        return {"uid": uid, "token": None}

    if uid and password:
        result = fetch_token(uid, password)
        if result["token"]:
            output_data.append(result)
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})

    if file_param:
        if not os.path.exists(file_param):
            return jsonify({"error": f"❌ File not found: {file_param}"}), 404
        try:
            with open(file_param, "r", encoding="utf-8") as f:
                content = f.read()
            pairs = re.findall(r'"uid"\s*:\s*"(\d+)"\s*,\s*"password"\s*:\s*"([A-Fa-f0-9]+)"', content)
            for uid, password in pairs:
                result = fetch_token(uid, password)
                if result["token"]:
                    output_data.append(result)
            output_file = os.path.join(os.path.dirname(file_param), "token_ind.json")
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(output_data, outfile, indent=4, ensure_ascii=False)
            return jsonify({"status": "success", "count": len(output_data), "output_file": output_file, "accounts": output_data})
        except Exception as e:
            return jsonify({"error": f"❌ Error processing file {file_param}: {e}"}), 500

    return jsonify({"error": "⚠️ Please provide either uid/password or file"}), 400

@app.route("/help", methods=["GET"])
def api_help():
    commands = {
        "/api/check?key=hentaiz&uid=<UID>": "Kiểm tra trạng thái tài khoản Free Fire",
        "/api/decode?key=hentaiz&token=<TOKEN>": "Decode token qua proxy",
        "/api/check_token_file?key=hentaiz&token_file=<TOKEN1>,<TOKEN2>": "Decode token trực tiếp (không verify chữ ký)",
        "/api/guest_accounts?key=hentaiz&file=<FILE>": "Đọc file guest account",
        "/api/guest_accounts?key=hentaiz&dir=<DIR>": "Quét toàn bộ file .dat trong thư mục",
        "/api/token?key=hentaiz&uid=<UID>&password=<PASS>": "Lấy token từ UID + password",
        "/api/token?key=hentaiz&file=<FILE>": "Lấy token từ file JSON",
        "/api/help": "Hiển thị danh sách lệnh"
    }
    return jsonify({
        "status": "ok",
        "message": "📖 Danh sách API có sẵn",
        "commands": commands,
        "base_url": "https://check-band-by-hentaiz-bc9o.vercel.app/"
    })
    
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5055)))
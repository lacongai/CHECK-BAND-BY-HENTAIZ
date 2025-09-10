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
@app.route("/api/check_token_file", methods=["POST", "GET"])
def check_token_file():
    key = request.args.get("key") or request.form.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    token_file = request.args.get("token_file") or request.form.get("token_file")
    uploaded_file = request.files.get("file")
    tokens = []

    # 📂 Nếu upload file
    if uploaded_file:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
        uploaded_file.save(tmp_path)
        if tmp_path.endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as zip_ref:
                extract_dir = tempfile.mkdtemp()
                zip_ref.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.endswith((".txt", ".json")):
                            with open(os.path.join(root, fn), "r", encoding="utf-8", errors="ignore") as f:
                                for line in f:
                                    token = line.strip().strip('"')
                                    if len(token) > 20:
                                        tokens.append(token)
        else:
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    token = line.strip().strip('"')
                    if len(token) > 20:
                        tokens.append(token)

    elif token_file:
        tokens.extend([t.strip().strip('"') for t in token_file.split(",") if len(t.strip()) > 20])
    else:
        return jsonify({"error": "❌ token_file parameter or file upload required"}), 400

    # 🔎 Decode
    results = []
    for idx, token in enumerate(tokens, start=1):
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
@app.route("/api/decode", methods=["POST", "GET"])
def api_decode_proxy():
    key = request.args.get("key") or request.form.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    token = request.args.get("token") or request.form.get("token")
    uploaded_file = request.files.get("file")
    tokens = []

    # 📌 Nếu upload file
    if uploaded_file:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
        uploaded_file.save(tmp_path)
        if tmp_path.endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as zip_ref:
                extract_dir = tempfile.mkdtemp()
                zip_ref.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.endswith((".txt", ".json")):
                            with open(os.path.join(root, fn), "r", encoding="utf-8", errors="ignore") as f:
                                for line in f:
                                    tk = line.strip().strip('"')
                                    if len(tk) > 20:
                                        tokens.append(tk)
        else:
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    tk = line.strip().strip('"')
                    if len(tk) > 20:
                        tokens.append(tk)

    elif token:
        tokens = [t.strip().strip('"') for t in token.split(",") if len(t.strip()) > 20]

    else:
        return jsonify({"error": "❌ token parameter or file upload required"}), 400

    # 📌 Proxy sang API decode gốc
    results = []
    for idx, tk in enumerate(tokens, start=1):
        try:
            url = f"https://check-token-nbau.vercel.app/api/check_token_file?key={API_KEY}&token_file={tk}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # ghép thêm index để đồng bộ format
                results.append({"index": idx, "status": "success", "raw": data})
            else:
                results.append({"index": idx, "status": "error", "message": f"❌ HTTP {response.status_code}"})
        except Exception as e:
            results.append({"index": idx, "status": "error", "message": f"❌ Exception: {str(e)}"})

    return jsonify({"results": results})
    
# ==============================
# Guest Accounts
# ==============================
@app.route("/api/guest_accounts", methods=["POST", "GET"])
def api_guest_accounts():
    key = request.args.get("key") or request.form.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    file_param = request.args.get("file") or request.form.get("file")
    dir_param = request.args.get("dir", ".")
    uploaded_file = request.files.get("file")
    output_data = []
    paths_to_scan = []

    # 📂 Nếu upload file
    if uploaded_file:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
        uploaded_file.save(tmp_path)
        paths_to_scan.append(tmp_path)
        if tmp_path.endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as zip_ref:
                extract_dir = tempfile.mkdtemp()
                zip_ref.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.endswith((".json", ".dat", ".txt")):
                            paths_to_scan.append(os.path.join(root, fn))
    elif file_param and os.path.exists(file_param):
        paths_to_scan.append(file_param)
    else:
        # 📂 Nếu quét thư mục
        if not os.path.exists(dir_param):
            return jsonify({"error": f"❌ Directory not found: {dir_param}"}), 404
        for fn in os.listdir(dir_param):
            if fn.endswith((".dat", ".json", ".txt")):
                paths_to_scan.append(os.path.join(dir_param, fn))

    # 🔎 Quét file
    for path in paths_to_scan:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            try:
                js = json.loads(content)
                guest_info = js.get("guest_account_info", {})
                uid = guest_info.get("com.garena.msdk.guest_uid", "").strip('"')
                password = guest_info.get("com.garena.msdk.guest_password", "").strip('"')
                if uid and password:
                    output_data.append({"file": path, "uid": uid, "password": password})
            except:
                # Regex fallback (bỏ " nếu có)
                matches = re.findall(r'uid["\']?\s*[:=]\s*["\']?(\d+)["\']?.*?password["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)', content, re.I)
                for u, p in matches:
                    output_data.append({"file": path, "uid": u, "password": p})
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")

    return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})
    
# ==============================
# Generate token từ uid/pass
# ==============================
@app.route("/api/token", methods=["POST", "GET"])
def api_token_generate():
    key = request.args.get("key") or request.form.get("key")
    if key != API_KEY:
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("password") or request.form.get("password")
    file_param = request.args.get("file") or request.form.get("file")
    uploaded_file = request.files.get("file")

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

    # 📌 Trường hợp nhập trực tiếp uid/pass
    if uid and password:
        result = fetch_token(uid.strip('"'), password.strip('"'))
        if result["token"]:
            output_data.append(result)
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})

    # 📌 Trường hợp upload file
    paths_to_scan = []
    if uploaded_file:
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
        uploaded_file.save(tmp_path)
        paths_to_scan.append(tmp_path)
        # Nếu file là ZIP → giải nén toàn bộ
        if tmp_path.endswith(".zip"):
            with zipfile.ZipFile(tmp_path, "r") as zip_ref:
                extract_dir = tempfile.mkdtemp()
                zip_ref.extractall(extract_dir)
                for root, _, files in os.walk(extract_dir):
                    for fn in files:
                        if fn.endswith((".json", ".dat", ".txt")):
                            paths_to_scan.append(os.path.join(root, fn))
    elif file_param and os.path.exists(file_param):
        paths_to_scan.append(file_param)

    # 📌 Quét file tìm UID/PASS
    for path in paths_to_scan:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Regex tìm UID + PASS (có hoặc không có dấu ")
            pairs = re.findall(r'uid["\']?\s*[:=]\s*["\']?(\d+)["\']?.*?password["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)["\']?', content, re.I)
            for u, p in pairs:
                result = fetch_token(u, p)
                if result["token"]:
                    output_data.append(result)
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")

    if output_data:
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})
    return jsonify({"error": "⚠️ No valid uid/password found"}), 404

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
from flask import Flask, request, Response
import requests
import json
import os

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY")  
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Decode token run" })
    
    
# ✅ Hàm lấy tên và vùng
def get_player_info(player_id):
    cookies = {
        'region': 'MA',
        'language': 'ar',
        'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',
    }

    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://shop2game.com',
        'Referer': 'https://shop2game.com/app/100067/idlogin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
    }

    json_data = {
        'app_id': 100067,
        'login_id': f'{player_id}',
        'app_server_id': 0,
    }

    try:
        res = requests.post('https://shop2game.com/api/auth/player_id_login',
                            cookies=cookies, headers=headers, json=json_data)
        if res.status_code == 200:
            data = res.json()
            return {
                "nickname": data.get("nickname", "❌ Không rõ"),
                "region": data.get("region", "❌ Không rõ")
            }
    except:
        pass

    return {
        "nickname": "❌ Không thể lấy tên",
        "region": "❌ Không thấy khu vực"
    }


# ✅ Hàm kiểm tra ban
def check_banned(player_id):
    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
        "Accept": "application/json",
        "referer": "https://ff.garena.com/en/support/",
        "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"
    }

    try:
        response = requests.get(url, headers=headers)
        player_info = get_player_info(player_id)

        if response.status_code == 200:
            data = response.json().get("data", {})
            is_banned = data.get("is_banned", 0)
            period = data.get("period", 0)

            if is_banned:
                if period > 0:
                    duration = f"{period} ngày"
                else:
                    duration = "Khoá vĩnh viễn"
            else:
                duration = "Không bị khóa"

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

            return Response(json.dumps(result, indent=4, ensure_ascii=False),
                            mimetype="application/json")

        else:
            return Response(json.dumps({
                "❌ lỗi": "Không thể lấy trạng thái cấm từ máy chủ Garena",
                "status_code": 500
            }, indent=4, ensure_ascii=False), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({
            "💥 exception": str(e),
            "status_code": 500
        }, indent=4, ensure_ascii=False), mimetype="application/json")


@app.route("/api/check", methods=["GET"])
def api_check():
    key = request.args.get("key")
    if key != "hentaiz":  # 🔑 check API key
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    player_id = request.args.get("uid")
    if not player_id:
        return jsonify({
            "error": "⚠️ Cần phải có ID người chơi (uid)!",
            "status_code": 400
        }), 400

    return check_banned(player_id)  # sửa trong check_banned cũng phải trả jsonify


import requests
from flask import request, jsonify

@app.route("/api/decode", methods=["GET"])
def api_decode_proxy():
    token = request.args.get("token")

    if key != "hentaiz":  # 🔑 check API key
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    if not token:
        return jsonify({"error": "❌ token parameter is required"}), 400

    try:
        # Gọi sang API decode thật ở Vercel
        url = f"https://check-token-nbau.vercel.app/api/check_token_file?key=hentaiz&token_file={token}"
        response = requests.get(url, timeout=10)

        # Nếu API kia trả về lỗi
        if response.status_code != 200:
            return jsonify({
                "results": [{
                    "index": 1,
                    "status": "error",
                    "message": f"❌ Upstream error {response.status_code}",
                    "decode_message": "❌ Proxy thất bại",
                    "expired": None,
                    "exp_time": None,
                    "payload": {},
                    "token": token
                }]
            }), response.status_code

        # Trả nguyên JSON kết quả
        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "results": [{
                "index": 1,
                "status": "error",
                "message": f"❌ Exception: {str(e)}",
                "decode_message": "❌ Proxy thất bại",
                "expired": None,
                "exp_time": None,
                "payload": {},
                "token": token
            }]
        }), 500
        

@app.route("/api/guest_accounts", methods=["GET"])
def api_guest_accounts():
    key = request.args.get("key")
    if key != "hentaiz":  # 🔑 bảo mật API key
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    file_param = request.args.get("file")
    dir_param = request.args.get("dir", ".")  

    output_data = []

    # ==============================
    # 1️⃣ Nếu truyền file cụ thể
    # ==============================
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

    # ==============================
    # 2️⃣ Nếu truyền dir → quét toàn bộ .dat
    # ==============================
    else:
        if not os.path.exists(dir_param):
            return jsonify({"error": f"❌ Directory not found: {dir_param}"}), 404

        dat_files = [f for f in os.listdir(dir_param) if f.endswith(".dat")]
        if not dat_files:
            return jsonify({"error": "❌ No .dat files found in directory"}), 404

        for dat_file in dat_files:
            dat_path = os.path.join(dir_param, dat_file)
            try:
                with open(dat_path, "r", encoding="utf-8") as f:
                    content = json.load(f)

                guest_info = content.get("guest_account_info", {})
                uid = guest_info.get("com.garena.msdk.guest_uid", "").strip()
                password = guest_info.get("com.garena.msdk.guest_password", "").strip()

                if uid and password:
                    output_data.append({"file": dat_file, "uid": uid, "password": password})
            except Exception as e:
                print(f"⚠️ Error reading {dat_file}: {e}")

    # ==============================
    # 3️⃣ Xuất kết quả ra file
    # ==============================
    output_file = os.path.join(dir_param, "ind_ind.json")
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        return jsonify({"error": f"❌ Error writing JSON file: {e}"}), 500

    return jsonify({
        "status": "success",
        "count": len(output_data),
        "output_file": output_file,
        "accounts": output_data
    })
        

@app.route("/api/token", methods=["GET"])
def api_token_generate():
    key = request.args.get("key")
    if key != "hentaiz":  # 🔑 check API key
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

    # 1️⃣ Nếu truyền trực tiếp uid + password
    if uid and password:
        result = fetch_token(uid, password)
        if result["token"]:
            output_data.append(result)
        return jsonify({"status": "success", "count": len(output_data), "accounts": output_data})

    # 2️⃣ Nếu truyền file chứa uid/password
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

            # Lưu ra file token_ind.json
            output_file = os.path.join(os.path.dirname(file_param), "token_ind.json")
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(output_data, outfile, indent=4, ensure_ascii=False)

            return jsonify({
                "status": "success",
                "count": len(output_data),
                "output_file": output_file,
                "accounts": output_data
            })

        except Exception as e:
            return jsonify({"error": f"❌ Error processing file {file_param}: {e}"}), 500

    return jsonify({"error": "⚠️ Please provide either uid/password or file"}), 400
    
                                                    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5055)))

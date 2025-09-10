# SOURCE VÀ API Ở DƯỚI CÓ THỂ BỊ LỖI KHÔNG HOẠT ĐỘNG 

# 📌 Check Band API  

API hỗ trợ kiểm tra trạng thái tài khoản game (bị ban hoặc không).  

**Base URL:**

## https://check-band-by-hentaiz-bc9o.vercel.app/

---

## 🔍 Cách Check ID Game  

- Lệnh cơ bản:

/api/check?key=hentaiz&uid=

/api/decode?key=hentaiz&token=

/api/guest_accounts?key=hentaiz&file=

/api/token?key=hentaiz&uid=&password=

- Ví dụ:

/api/check?uid={IdGame}

/api/decode?key=hentaiz&token={jwt}

/api/guest_accounts?key=hentaiz&file={filename}

/api/token?key=hentaiz&uid=123456789&password=abcdef123

- API Kiểm Tra:  
## 👉 [https://check-band-by-hentaiz-bc9o.vercel.app/api/check?key=hentaiz&uid=3269229643](https://check-band-by-hentaiz-bc9o.vercel.app/api/check?key=hentaiz&uid=3269229643)

## 👉 [https://check-band-by-hentaiz-bc9o.vercel.app/api/decode?key=hentaiz&token=eyJhbGciOi...](https://check-band-by-hentaiz-bc9o.vercel.app/api/decode?key=hentaiz&token=eyJhbGciOi...)

## 👉 [https://check-band-by-hentaiz-bc9o.vercel.app/api/guest_accounts?key=hentaiz&file=fuck.json](https://check-band-by-hentaiz-bc9o.vercel.app/api/guest_accounts?key=hentaiz&file=fuck.json)

## 👉 [https://check-band-by-hentaiz-bc9o.vercel.app/api/guest_accounts?key=hentaiz&dir=/path/to/dir](https://check-band-by-hentaiz-bc9o.vercel.app/api/guest_accounts?key=hentaiz&dir=/path/to/dir)

# + Mặc Định File Trả Về : ind_ind.json

---

## ✅ Ví Dụ Kết Quả Trả Về Tài Khoản Không Bị Ban  

```json
{
    "✅ status": "Kiểm tra thành công",
    "🆔 UID": "3269229643",
    "🏷️ Nickname": "❌ Không thể lấy tên",
    "🌍 Region": "❌ Không thấy khu vực",
    "🔒 Account": "✅ BÌNH THƯỜNG",
    "⏳ Duration": "Không bị khóa",
    "📊 Banned?": false,
    "💎 Powered by": "t.me/@henntaiiz"
}
```

---

## 🚫 Ví Dụ Kết Quả Trả Về Tài Khoản Bị Ban

```json
{
    "✅ status": "Kiểm tra thành công",
    "🆔 UID": "3269229643",
    "🏷️ Nickname": "❌ Không thể lấy tên",
    "🌍 Region": "❌ Không thấy khu vực",
    "🔒 Account": "🚫 BỊ KHOÁ",
    "⏳ Duration": "7 ngày",
    "📊 Banned?": true,
    "💎 Powered by": "t.me/@henntaiiz"
}
```
---

## ✅ Ví Dụ Kết Quả Trả Về Decode

```json
{
  "results": [
    {
      "index": 1,
      "status": "success",
      "message": "Token valid until 2025-09-15 15:30:00",
      "decode_message": "✅ Token decode thành công",
      "expired": false,
      "exp_time": "2025-09-15 15:30:00",
      "payload": {
        "account_id": 12988618912,
        "nickname": "Kelly-Like_#",
        "client_version": "1.108.3",
        "country_code": "IN",
        "is_emulator": true,
        "exp": 1757931000
      },
      "token": "eyJhbGciOi..."
    }
  ]
}
```

---

## 🚫 Ví Dụ Kết Quả Trả Về Decode 

```json
{
  "results": [
    {
      "index": 1,
      "status": "success",
      "message": "Token expired at 2025-09-01 10:42:53",
      "decode_message": "✅ Token decode thành công",
      "expired": true,
      "exp_time": "2025-09-01 10:42:53",
      "payload": {
        "account_id": 12988618912,
        "nickname": "Kelly-Like_#",
        "client_version": "1.108.3",
        "country_code": "IN",
        "is_emulator": true,
        "exp": 1756698173
      },
      "token": "eyJhbGciOi..."
    }
  ]
}
```
---

## ✅ Ví Dụ Kết Quả Trả Về Đọc File Guest_Accounts thành công

```json
{
  "status": "success",
  "count": 1,
  "output_file": "./ind_ind.json",
  "accounts": [
    {
      "file": "fuck.json",
      "uid": "123456789",
      "password": "abc123"
    }
  ]
}
```

---

## 🚫 Ví Dụ Kết Quả Trả Về Đọc File Guest_Accounts Thất Bại

```json
{
  "error": "❌ File not found: fuck.json"
}
```
---

## ✅ Ví Dụ Kết Quả Trả Về Đọc File .dat thành công

```json
{
  "status": "success",
  "count": 2,
  "output_file": "./ind_ind.json",
  "accounts": [
    {
      "file": "guest1.dat",
      "uid": "987654321",
      "password": "xyz789"
    },
    {
      "file": "guest2.dat",
      "uid": "1122334455",
      "password": "pass5566"
    }
  ]
}
```

---

## 🚫 Ví Dụ Kết Quả Trả Về Đọc File .dat Thất Bại

```json
{
  "error": "❌ No .dat files found in directory"
}
```

## 🔐 Thông Báo Key Sau

```
{
  "error": "❌ Unauthorized. Invalid key!"
}
```

## ✅ Ví Dụ Kết Quả Trả Về Lấy Token thành công

```json
{
  "status": "success",
  "count": 2,
  "output_file": "./token_ind.json",
  "accounts": [
    { "uid": "123456789", "token": "eyJhbGciOi..." },
    { "uid": "987654321", "token": "eyJhbGciOi..." }
  ]
}
```

---

## 🚫 Ví Dụ Kết Quả Trả Về Lấy Token Thất Bại

```json
{
  "error": "⚠️ Please provide either uid/password or file"
}
or
{
  "error": "❌ File not found: fuck.json"
}
or
{
  "status": "success",
  "count": 0,
  "output_file": "./token_ind.json",
  "accounts": []
}
```

---

## 🖥️ Hướng Dẫn Tích Hợp API


## 1. Python (requests)

```python
import requests
import json

API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app"
API_KEY = "hentaiz"

# ================================
# 1️⃣ Check Free Fire Account
# ================================
uid = "3269229643"
url_check = f"{API_BASE}/api/check?uid={uid}&key={API_KEY}"

try:
    res = requests.get(url_check).json()
    print("=== Free Fire Account Check ===")
    print("UID:", res.get("🆔 UID"))
    print("Trạng thái:", res.get("🔒 Account"))
    print("Bị ban:", res.get("📊 Banned?"))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print()
except Exception as e:
    print("❌ Lỗi khi gọi API /api/check:", e)

# ================================
# 2️⃣ Decode Token
# ================================
token = "eyJhbGciOi..."  # thay bằng token thật
url_decode = f"{API_BASE}/api/decode?key={API_KEY}&token={token}"

try:
    res = requests.get(url_decode).json()
    print("=== Token Decode ===")
    if "results" in res:
        for r in res["results"]:
            print(f"📊 Token #{r['index']}")
            print("Trạng thái:", r["status"])
            print("Thông điệp:", r["message"])
            print("Hết hạn?:", r["expired"])
            print("Hết hạn lúc:", r["exp_time"])
            print("Payload:", json.dumps(r["payload"], indent=2, ensure_ascii=False))
            print()
    else:
        print(res)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print()
except Exception as e:
    print("❌ Lỗi khi gọi API /api/decode:", e)

# ================================
# 3️⃣ Guest Accounts
# ================================
url_guest = f"{API_BASE}/api/guest_accounts?key={API_KEY}&file=fuck.json"

try:
    res = requests.get(url_guest).json()
    print("=== Guest Accounts ===")
    print("Status:", res.get("status"))
    print("Số account:", res.get("count"))
    for acc in res.get("accounts", []):
        print(f"File: {acc.get('file')}")
        print(f"UID: {acc.get('uid')}")
        print(f"Password: {acc.get('password')}\n")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print()
except Exception as e:
    print("❌ Lỗi khi gọi API /api/guest_accounts:", e)

# ================================
# 4️⃣ Generate Tokens
# ================================
url_token = f"{API_BASE}/api/token?key={API_KEY}&file=fuck.json"

try:
    res = requests.get(url_token).json()
    print("=== Generate Tokens ===")
    print("Status:", res.get("status"))
    print("Số token:", res.get("count"))
    for acc in res.get("accounts", []):
        print(f"UID: {acc.get('uid')}")
        print(f"Token: {acc.get('token')}\n")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print()
except Exception as e:
    print("❌ Lỗi khi gọi API /api/token:", e)
    
```

---

## 2. JavaScript (Fetch API – dùng trên web)

```JavaScript
const API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app";
const API_KEY = "hentaiz";

// =============================
// 1️⃣ Check Free Fire Account
// =============================
fetch(`${API_BASE}/api/check?uid=3269229643&key=${API_KEY}`)
  .then(response => response.json())
  .then(data => {
    console.log("=== Free Fire Account Check ===");
    console.log("UID:", data["🆔 UID"]);
    console.log("Trạng thái:", data["🔒 Account"]);
    console.log("Bị ban:", data["📊 Banned?"]);
    console.log(JSON.stringify(data, null, 2));
    console.log("\n");
  })
  .catch(error => console.error("❌ Lỗi /api/check:", error));

// =============================
// 2️⃣ Decode Token
// =============================
const token = "eyJhbGciOi..."; // thay bằng token thật
fetch(`${API_BASE}/api/decode?key=${API_KEY}&token=${encodeURIComponent(token)}`)
  .then(response => response.json())
  .then(data => {
    console.log("=== Token Decode ===");
    if (data.results) {
      data.results.forEach(r => {
        console.log(`📊 Token #${r.index}`);
        console.log("Trạng thái:", r.status);
        console.log("Thông điệp:", r.message);
        console.log("Hết hạn?:", r.expired);
        console.log("Hết hạn lúc:", r.exp_time);
        console.log("Payload:", JSON.stringify(r.payload, null, 2));
        console.log("-------------------------");
      });
    } else {
      console.log(data);
    }
    console.log(JSON.stringify(data, null, 2));
    console.log("\n");
  })
  .catch(error => console.error("❌ Lỗi /api/decode:", error));

// =============================
// 3️⃣ Guest Accounts
// =============================
fetch(`${API_BASE}/api/guest_accounts?key=${API_KEY}&file=fuck.json`)
  .then(response => response.json())
  .then(data => {
    console.log("=== Guest Accounts ===");
    console.log("Status:", data.status);
    console.log("Số account:", data.count);
    if (data.accounts) {
      data.accounts.forEach(acc => {
        console.log(`File: ${acc.file}`);
        console.log(`UID: ${acc.uid}`);
        console.log(`Password: ${acc.password}`);
        console.log("-------------------------");
      });
    }
    console.log(JSON.stringify(data, null, 2));
    console.log("\n");
  })
  .catch(error => console.error("❌ Lỗi /api/guest_accounts:", error));

// =============================
// 4️⃣ Generate Tokens
// =============================
fetch(`${API_BASE}/api/token?key=${API_KEY}&file=fuck.json`)
  .then(response => response.json())
  .then(data => {
    console.log("=== Generate Tokens ===");
    console.log("Status:", data.status);
    console.log("Số token:", data.count);
    if (data.accounts) {
      data.accounts.forEach(acc => {
        console.log(`UID: ${acc.uid}`);
        console.log(`Token: ${acc.token}`);
        console.log("-------------------------");
      });
    }
    console.log(JSON.stringify(data, null, 2));
    console.log("\n");
  })
  .catch(error => console.error("❌ Lỗi /api/token:", error));
  
```

---

## 3. Node.js (Axios)

```js
const axios = require("axios");

const API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app";
const API_KEY = "hentaiz";

(async () => {
  try {
    // ================================
    // 1️⃣ Check Free Fire Account
    // ================================
    const uid = "3269229643";
    const res1 = await axios.get(`${API_BASE}/api/check`, {
      params: { uid, key: API_KEY }
    });

    console.log("=== Free Fire Account Check ===");
    console.log(JSON.stringify(res1.data, null, 2));
    console.log();

    // ================================
    // 2️⃣ Decode Token
    // ================================
    const token = "eyJhbGciOi..."; // thay bằng token thật
    const res2 = await axios.get(`${API_BASE}/api/decode`, {
      params: { key: API_KEY, token }
    });

    console.log("=== Token Decode ===");
    console.log(JSON.stringify(res2.data, null, 2));
    console.log();

    // ================================
    // 3️⃣ Guest Accounts
    // ================================
    const res3 = await axios.get(`${API_BASE}/api/guest_accounts`, {
      params: { key: API_KEY, file: "fuck.json" }
    });

    console.log("=== Guest Accounts ===");
    console.log(JSON.stringify(res3.data, null, 2));
    console.log();

    // ================================
    // 4️⃣ Generate Tokens
    // ================================
    const res4 = await axios.get(`${API_BASE}/api/token`, {
      params: { key: API_KEY, file: "fuck.json" }
    });

    console.log("=== Generate Tokens ===");
    console.log(JSON.stringify(res4.data, null, 2));
    console.log();

  } catch (err) {
    if (err.response) {
      console.error("❌ API Error:", err.response.data);
    } else {
      console.error("❌ Request Error:", err.message);
    }
  }
})();

```

---

## 4. Telegram Bot (Python – dùng python-telegram-bot)

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app"
API_KEY = "hentaiz"

# ================================
# 1️⃣ /check <uid>
# ================================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập UID. Ví dụ: /check 3269229643")
        return

    uid = context.args[0]
    url = f"{API_BASE}/api/check?uid={uid}&key={API_KEY}"

    try:
        res = requests.get(url).json()
        reply = (
            f"✅ Kết quả kiểm tra:\n"
            f"🆔 UID: {res.get('🆔 UID')}\n"
            f"🔒 Trạng thái: {res.get('🔒 Account')}\n"
            f"📊 Banned?: {res.get('📊 Banned?')}\n"
            f"💎 Powered by: {res.get('💎 Powered by')}"
        )
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi gọi API /check: {e}")

# ================================
# 2️⃣ /decode <token>
# ================================
async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập token. Ví dụ: /decode eyJhbGciOi...")
        return

    token = context.args[0]
    url = f"{API_BASE}/api/decode?key={API_KEY}&token={token}"

    try:
        res = requests.get(url).json()
        if "results" in res:
            reply_parts = []
            for r in res["results"]:
                reply_parts.append(
                    f"📊 Token #{r['index']}\n"
                    f"Trạng thái: {r['status']}\n"
                    f"Thông điệp: {r['message']}\n"
                    f"Hết hạn?: {r['expired']}\n"
                    f"Hết hạn lúc: {r['exp_time']}\n"
                    f"👤 Nickname: {r['payload'].get('nickname')}"
                )
            reply = "\n\n".join(reply_parts)
        else:
            reply = f"❌ Lỗi: {res}"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi gọi API /decode: {e}")

# ================================
# 3️⃣ /guest <file>
# ================================
async def guest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập file JSON. Ví dụ: /guest fuck.json")
        return

    file_name = context.args[0]
    url = f"{API_BASE}/api/guest_accounts?key={API_KEY}&file={file_name}"

    try:
        res = requests.get(url).json()
        if res.get("status") == "success":
            reply_parts = [f"📂 Guest Accounts ({res.get('count')})"]
            for acc in res.get("accounts", []):
                reply_parts.append(
                    f"UID: {acc.get('uid')} | Pass: {acc.get('password')}"
                )
            reply = "\n".join(reply_parts)
        else:
            reply = f"❌ Lỗi: {res}"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi gọi API /guest: {e}")

# ================================
# 4️⃣ /gentoken <file>
# ================================
async def gentoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập file JSON. Ví dụ: /gentoken fuck.json")
        return

    file_name = context.args[0]
    url = f"{API_BASE}/api/token?key={API_KEY}&file={file_name}"

    try:
        res = requests.get(url).json()
        if res.get("status") == "success":
            reply_parts = [f"🔑 Tokens ({res.get('count')})"]
            for acc in res.get("accounts", []):
                reply_parts.append(
                    f"UID: {acc.get('uid')}\nToken: {acc.get('token')}\n"
                )
            reply = "\n".join(reply_parts)
        else:
            reply = f"❌ Lỗi: {res}"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi gọi API /gentoken: {e}")

# ================================
# 🚀 Run bot
# ================================
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("decode", decode))
app.add_handler(CommandHandler("guest", guest))
app.add_handler(CommandHandler("gentoken", gentoken))

print("🤖 Bot đang chạy...")
app.run_polling()

```

---

## 5. Telegram Bot (Node.js – dùng telegraf)

```js
const { Telegraf } = require("telegraf");
const axios = require("axios");

const bot = new Telegraf("YOUR_TELEGRAM_BOT_TOKEN");

const API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app";
const API_KEY = "hentaiz";

// =============================
// 1️⃣ /check <uid>
// =============================
bot.command("check", async (ctx) => {
  const args = ctx.message.text.split(" ");
  if (args.length < 2) {
    return ctx.reply("Vui lòng nhập UID. Ví dụ: /check 3269229643");
  }

  const uid = args[1];
  const url = `${API_BASE}/api/check?uid=${uid}&key=${API_KEY}`;

  try {
    const res = await axios.get(url);
    const data = res.data;

    ctx.reply(
      `✅ Kết quả kiểm tra:\n` +
      `🆔 UID: ${data["🆔 UID"]}\n` +
      `🔒 Trạng thái: ${data["🔒 Account"]}\n` +
      `📊 Banned?: ${data["📊 Banned?"]}\n` +
      `💎 Powered by: ${data["💎 Powered by"]}`
    );
  } catch (err) {
    ctx.reply("❌ Lỗi khi kiểm tra API /api/check.");
  }
});

// =============================
// 2️⃣ /decode <token>
// =============================
bot.command("decode", async (ctx) => {
  const args = ctx.message.text.split(" ");
  if (args.length < 2) {
    return ctx.reply("Vui lòng nhập token. Ví dụ: /decode eyJhbGciOi...");
  }

  const token = args[1];
  const url = `${API_BASE}/api/decode?key=${API_KEY}&token=${encodeURIComponent(token)}`;

  try {
    const res = await axios.get(url);
    const data = res.data;

    if (data.results) {
      let reply = "";
      data.results.forEach(r => {
        reply +=
          `📊 Token #${r.index}\n` +
          `Trạng thái: ${r.status}\n` +
          `Thông điệp: ${r.message}\n` +
          `Hết hạn?: ${r.expired}\n` +
          `Hết hạn lúc: ${r.exp_time}\n\n`;
      });
      ctx.reply(reply.trim());
    } else {
      ctx.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
    }
  } catch (err) {
    ctx.reply("❌ Lỗi khi kiểm tra API /api/decode.");
  }
});

// =============================
// 3️⃣ /guest <file>
// =============================
bot.command("guest", async (ctx) => {
  const args = ctx.message.text.split(" ");
  if (args.length < 2) {
    return ctx.reply("Vui lòng nhập file. Ví dụ: /guest fuck.json");
  }

  const file = args[1];
  const url = `${API_BASE}/api/guest_accounts?key=${API_KEY}&file=${file}`;

  try {
    const res = await axios.get(url);
    const data = res.data;

    if (data.status === "success") {
      let reply = `📂 Guest Accounts (${data.count})\n\n`;
      data.accounts.forEach(acc => {
        reply += `UID: ${acc.uid}\nPassword: ${acc.password}\n\n`;
      });
      ctx.reply(reply.trim());
    } else {
      ctx.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
    }
  } catch (err) {
    ctx.reply("❌ Lỗi khi gọi API /api/guest_accounts.");
  }
});

// =============================
// 4️⃣ /gentoken <file>
// =============================
bot.command("gentoken", async (ctx) => {
  const args = ctx.message.text.split(" ");
  if (args.length < 2) {
    return ctx.reply("Vui lòng nhập file. Ví dụ: /gentoken fuck.json");
  }

  const file = args[1];
  const url = `${API_BASE}/api/token?key=${API_KEY}&file=${file}`;

  try {
    const res = await axios.get(url);
    const data = res.data;

    if (data.status === "success") {
      let reply = `🔑 Tokens (${data.count})\n\n`;
      data.accounts.forEach(acc => {
        reply += `UID: ${acc.uid}\nToken: ${acc.token}\n\n`;
      });
      ctx.reply(reply.trim());
    } else {
      ctx.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
    }
  } catch (err) {
    ctx.reply("❌ Lỗi khi gọi API /api/token.");
  }
});

// =============================
// 🚀 Run Bot
// =============================
bot.launch();
console.log("🤖 Bot đang chạy...");

```

---

## 6. Discord Bot (Node.js – dùng discord.js)

```js
const { Client, GatewayIntentBits } = require("discord.js");
const axios = require("axios");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const TOKEN = "YOUR_DISCORD_BOT_TOKEN";
const API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app";
const API_KEY = "hentaiz";

client.on("ready", () => {
  console.log(`🤖 Bot đã đăng nhập thành công dưới tên ${client.user.tag}`);
});

client.on("messageCreate", async (message) => {
  if (message.author.bot) return;

  const args = message.content.split(" ");
  const cmd = args[0];

  // ============================
  // 1️⃣ !check <uid>
  // ============================
  if (cmd === "!check") {
    if (args.length < 2) {
      return message.reply("Vui lòng nhập UID. Ví dụ: `!check 3269229643`");
    }
    const uid = args[1];
    const url = `${API_BASE}/api/check?uid=${uid}&key=${API_KEY}`;

    try {
      const { data } = await axios.get(url);
      message.reply(
        `✅ Kết quả kiểm tra:\n` +
        `🆔 UID: ${data["🆔 UID"]}\n` +
        `🔒 Trạng thái: ${data["🔒 Account"]}\n` +
        `📊 Banned?: ${data["📊 Banned?"]}\n` +
        `💎 Powered by: ${data["💎 Powered by"]}`
      );
    } catch {
      message.reply("❌ Lỗi khi gọi API /api/check.");
    }
  }

  // ============================
  // 2️⃣ !decode <token>
  // ============================
  if (cmd === "!decode") {
    if (args.length < 2) {
      return message.reply("Vui lòng nhập token. Ví dụ: `!decode eyJhbGciOi...`");
    }
    const token = args[1];
    const url = `${API_BASE}/api/decode?key=${API_KEY}&token=${encodeURIComponent(token)}`;

    try {
      const { data } = await axios.get(url);
      if (data.results) {
        let reply = "";
        data.results.forEach(r => {
          reply +=
            `📊 Token #${r.index}\n` +
            `Trạng thái: ${r.status}\n` +
            `Thông điệp: ${r.message}\n` +
            `Hết hạn?: ${r.expired}\n` +
            `Hết hạn lúc: ${r.exp_time}\n\n`;
        });
        message.reply(reply.trim());
      } else {
        message.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
      }
    } catch {
      message.reply("❌ Lỗi khi gọi API /api/decode.");
    }
  }

  // ============================
  // 3️⃣ !guest <file>
  // ============================
  if (cmd === "!guest") {
    if (args.length < 2) {
      return message.reply("Vui lòng nhập tên file. Ví dụ: `!guest fuck.json`");
    }
    const file = args[1];
    const url = `${API_BASE}/api/guest_accounts?key=${API_KEY}&file=${file}`;

    try {
      const { data } = await axios.get(url);
      if (data.status === "success") {
        let reply = `📂 Guest Accounts (${data.count})\n\n`;
        data.accounts.forEach(acc => {
          reply += `UID: ${acc.uid}\nPassword: ${acc.password}\n\n`;
        });
        message.reply(reply.trim());
      } else {
        message.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
      }
    } catch {
      message.reply("❌ Lỗi khi gọi API /api/guest_accounts.");
    }
  }

  // ============================
  // 4️⃣ !gentoken <file>
  // ============================
  if (cmd === "!gentoken") {
    if (args.length < 2) {
      return message.reply("Vui lòng nhập tên file. Ví dụ: `!gentoken fuck.json`");
    }
    const file = args[1];
    const url = `${API_BASE}/api/token?key=${API_KEY}&file=${file}`;

    try {
      const { data } = await axios.get(url);
      if (data.status === "success") {
        let reply = `🔑 Tokens (${data.count})\n\n`;
        data.accounts.forEach(acc => {
          reply += `UID: ${acc.uid}\nToken: ${acc.token}\n\n`;
        });
        message.reply(reply.trim());
      } else {
        message.reply(`❌ Lỗi: ${JSON.stringify(data)}`);
      }
    } catch {
      message.reply("❌ Lỗi khi gọi API /api/token.");
    }
  }
});

client.login(TOKEN);

```

---

## 7. Discord Bot (Python – dùng discord.py)

```python
import discord
import requests

TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app"
API_KEY = "hentaiz"

@client.event
async def on_ready():
    print(f"🤖 Bot đã đăng nhập thành công dưới tên {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    args = message.content.split(" ", 1)
    cmd = args[0]

    # ============================
    # 1️⃣ !check <uid>
    # ============================
    if cmd == "!check":
        if len(args) < 2:
            await message.channel.send("Vui lòng nhập UID. Ví dụ: `!check 3269229643`")
            return

        uid = args[1]
        url = f"{API_BASE}/api/check?uid={uid}&key={API_KEY}"

        try:
            res = requests.get(url).json()
            reply = (
                f"✅ Kết quả kiểm tra:\n"
                f"🆔 UID: {res.get('🆔 UID')}\n"
                f"🔒 Trạng thái: {res.get('🔒 Account')}\n"
                f"📊 Banned?: {res.get('📊 Banned?')}\n"
                f"💎 Powered by: {res.get('💎 Powered by')}"
            )
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"❌ Lỗi khi gọi API /api/check: {e}")

    # ============================
    # 2️⃣ !decode <token>
    # ============================
    if cmd == "!decode":
        if len(args) < 2:
            await message.channel.send("Vui lòng nhập token. Ví dụ: `!decode eyJhbGciOi...`")
            return

        token = args[1]
        url = f"{API_BASE}/api/decode?key={API_KEY}&token={token}"

        try:
            res = requests.get(url).json()
            if "results" in res:
                reply_parts = []
                for r in res["results"]:
                    reply_parts.append(
                        f"📊 Token #{r['index']}\n"
                        f"Trạng thái: {r['status']}\n"
                        f"Thông điệp: {r['message']}\n"
                        f"Hết hạn?: {r['expired']}\n"
                        f"Hết hạn lúc: {r['exp_time']}\n"
                        f"👤 Nickname: {r['payload'].get('nickname')}"
                    )
                reply = "\n\n".join(reply_parts)
            else:
                reply = f"❌ Lỗi: {res}"
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"❌ Lỗi khi gọi API /api/decode: {e}")

    # ============================
    # 3️⃣ !guest <file>
    # ============================
    if cmd == "!guest":
        if len(args) < 2:
            await message.channel.send("Vui lòng nhập file. Ví dụ: `!guest fuck.json`")
            return

        file = args[1]
        url = f"{API_BASE}/api/guest_accounts?key={API_KEY}&file={file}"

        try:
            res = requests.get(url).json()
            if res.get("status") == "success":
                reply_parts = [f"📂 Guest Accounts ({res.get('count')})"]
                for acc in res.get("accounts", []):
                    reply_parts.append(f"UID: {acc.get('uid')} | Pass: {acc.get('password')}")
                reply = "\n".join(reply_parts)
            else:
                reply = f"❌ Lỗi: {res}"
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"❌ Lỗi khi gọi API /api/guest_accounts: {e}")

    # ============================
    # 4️⃣ !gentoken <file>
    # ============================
    if cmd == "!gentoken":
        if len(args) < 2:
            await message.channel.send("Vui lòng nhập file. Ví dụ: `!gentoken fuck.json`")
            return

        file = args[1]
        url = f"{API_BASE}/api/token?key={API_KEY}&file={file}"

        try:
            res = requests.get(url).json()
            if res.get("status") == "success":
                reply_parts = [f"🔑 Tokens ({res.get('count')})"]
                for acc in res.get("accounts", []):
                    reply_parts.append(f"UID: {acc.get('uid')}\nToken: {acc.get('token')}")
                reply = "\n\n".join(reply_parts)
            else:
                reply = f"❌ Lỗi: {res}"
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"❌ Lỗi khi gọi API /api/token: {e}")

client.run(TOKEN)

```

---

## 8. Website UI (HTML + Fetch API)

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Check API Demo</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, sans-serif;
      background: #121212;
      color: #e0e0e0;
      text-align: center;
      padding: 20px;
      transition: background 0.3s, color 0.3s;
    }
    body.light {
      background: #f5f5f5;
      color: #222;
    }
    h1 {
      color: #00e676;
    }
    .card {
      background: #1e1e1e;
      border-radius: 10px;
      padding: 20px;
      margin: 20px auto;
      max-width: 600px;
      box-shadow: 0 0 15px rgba(0, 255, 100, 0.3);
      transition: background 0.3s, box-shadow 0.3s;
    }
    body.light .card {
      background: #fff;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    input, textarea, button {
      width: 90%;
      margin: 8px 0;
      padding: 10px;
      border: none;
      border-radius: 6px;
      font-size: 14px;
      transition: background 0.3s, color 0.3s;
    }
    input, textarea {
      background: #2c2c2c;
      color: #fff;
    }
    body.light input,
    body.light textarea {
      background: #f0f0f0;
      color: #000;
    }
    button {
      background: #00e676;
      color: #000;
      cursor: pointer;
      font-weight: bold;
      transition: 0.2s;
    }
    button:hover {
      background: #00c853;
    }
    pre {
      text-align: left;
      background: #000;
      color: #00e676;
      padding: 15px;
      border-radius: 6px;
      overflow-x: auto;
      max-height: 300px;
      transition: background 0.3s, color 0.3s;
    }
    body.light pre {
      background: #f0f0f0;
      color: #222;
    }
    #theme-toggle {
      position: fixed;
      top: 15px;
      right: 15px;
      padding: 10px 15px;
      border-radius: 50%;
      font-size: 18px;
      border: none;
      cursor: pointer;
      background: #00e676;
      color: #000;
    }
  </style>
</head>
<body>
  <button id="theme-toggle">🌙</button>
  <h1>🔍 API BY HENTAIZ</h1>

  <div class="card">
    <h3>1️⃣ Check Free Fire Account</h3>
    <input type="text" id="uid" placeholder="Nhập UID...">
    <button onclick="checkUID()">Kiểm Tra</button>
    <pre id="result-uid"></pre>
  </div>

  <div class="card">
    <h3>2️⃣ Decode Token</h3>
    <textarea id="token" rows="4" placeholder="Nhập token..."></textarea>
    <button onclick="decodeToken()">Decode</button>
    <pre id="result-token"></pre>
  </div>

  <div class="card">
    <h3>3️⃣ Guest Accounts</h3>
    <input type="text" id="guest-file" placeholder="Tên file JSON (vd: fuck.json)">
    <button onclick="guestAccounts()">Lấy Accounts</button>
    <pre id="result-guest"></pre>
  </div>

  <div class="card">
    <h3>4️⃣ Generate Tokens</h3>
    <input type="text" id="token-file" placeholder="Tên file JSON (vd: fuck.json)">
    <button onclick="generateTokens()">Generate</button>
    <pre id="result-gentoken"></pre>
  </div>

  <script>
    const API_BASE = "https://check-band-by-hentaiz-bc9o.vercel.app";
    const API_KEY = "hentaiz";

    async function checkUID() {
      const uid = document.getElementById("uid").value;
      if (!uid) return alert("Nhập UID!");
      const url = `${API_BASE}/api/check?uid=${uid}&key=${API_KEY}`;
      await callAPI(url, "result-uid");
    }

    async function decodeToken() {
      const token = document.getElementById("token").value;
      if (!token) return alert("Nhập token!");
      const url = `${API_BASE}/api/decode?key=${API_KEY}&token=${encodeURIComponent(token)}`;
      await callAPI(url, "result-token");
    }

    async function guestAccounts() {
      const file = document.getElementById("guest-file").value;
      if (!file) return alert("Nhập tên file!");
      const url = `${API_BASE}/api/guest_accounts?key=${API_KEY}&file=${file}`;
      await callAPI(url, "result-guest");
    }

    async function generateTokens() {
      const file = document.getElementById("token-file").value;
      if (!file) return alert("Nhập tên file!");
      const url = `${API_BASE}/api/token?key=${API_KEY}&file=${file}`;
      await callAPI(url, "result-gentoken");
    }

    async function callAPI(url, elementId) {
      try {
        const res = await fetch(url);
        const data = await res.json();
        document.getElementById(elementId).textContent =
          JSON.stringify(data, null, 2);
      } catch {
        document.getElementById(elementId).textContent = "❌ Lỗi khi gọi API.";
      }
    }

    // 🌙 Theme toggle + lưu vào localStorage
    const btn = document.getElementById("theme-toggle");
    function applyTheme(theme) {
      document.body.classList.toggle("light", theme === "light");
      btn.textContent = theme === "light" ? "🌞" : "🌙";
      localStorage.setItem("theme", theme);
    }
    btn.addEventListener("click", () => {
      const newTheme = document.body.classList.contains("light") ? "dark" : "light";
      applyTheme(newTheme);
    });
    // Load theme từ localStorage khi vào lại web
    const savedTheme = localStorage.getItem("theme") || "dark";
    applyTheme(savedTheme);
  </script>
</body>
</html>

👉 Mở file .html này trong trình duyệt là bạn có ngay giao diện nhập UID để check.

```

---

## 9.Link Download Termux

## https://t.me/ummedkhati/6399

---

## 10.Lệnh Setup (Chạy Trên Termux)

```
pkg update -y && pkg upgrade -y
pkg install python -y
pkg update && pkg upgrade -y
pkg install nodejs git -y
pkg install git -y
pip install python-telegram-bot requests
pip install telebot rich
pkg install boxes ruby -y
gem install lolcat
pip install pystyle
pkg install python git curl wget neofetch figlet toilet ruby boxes -y
pip install rich colorama
npm install discord.js
pip install yt_dlp

pip install telethon
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
pip install python-telegram-bot==20.3 aiohttp rich pytz
pip install requests beautifulsoup4
termux-setup-storage
pip install pywebview

claer
pip install python-telegram-bot[job-queue]
pip install --upgrade "python-telegram-bot[job-queue]"
pip install --upgrade pip
pip install pillow
npm install express cors

termux-wake-lock
npm i express cors
npm uninstall express

cd "Đường dãn tới file"

```
## Ví dụ dùng Python
python app.py

---
## 📊 Thông Tin

# API miễn phí sử dụng.

# Trả về dữ liệu JSON dễ dàng tích hợp vào bot, tool, hoặc website.

# Powered by:
## https://t.me/@henntaiiz



---

## 📌 Vậy là trong `README.md` đã có hướng dẫn:  
- Link Download Termux
- Lệnh Setup Termux
- JSON mẫu  
- Code Python, JS, Node.js  
- Telegram Bot (Python + Node.js)  
- Discord Bot (Python + Node.js)  
- Website UI (HTML + Fetch API)  

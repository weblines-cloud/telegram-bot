"""
Weblines starter: a minimal Telegram bot.

- Long polling (no webhook, no public URL needed).
- /start greets (in Persian), any other text is echoed back.
- GET /health on $PORT (default 3000) so the platform sees it as healthy.

Only the standard library: nothing to install, small image, fast build.
Set TELEGRAM_BOT_TOKEN (Weblines sets it for you from the create form).
"""

import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
PORT = int(os.environ.get("PORT", "3000"))
API = f"https://api.telegram.org/bot{TOKEN}"

state = {"ok": False, "username": None}


def call(method, payload=None, timeout=40):
    data = json.dumps(payload or {}).encode()
    req = urllib.request.Request(
        f"{API}/{method}", data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read())
    if not body.get("ok"):
        raise RuntimeError(body.get("description", "telegram error"))
    return body["result"]


START_TEXT = (
    "سلام {name}! 👋\n"
    "این یک ربات نمونه است که روی وب‌لاینز اجرا می‌شود.\n"
    "هر پیامی بفرستی، همان را برایت برمی‌گردانم.\n\n"
    "برای ساختن ربات خودت، این ریپو را fork کن و تابع handle را در bot.py تغییر بده:\n"
    "https://github.com/weblines-cloud/telegram-bot"
)


def reply(chat_id, text):
    call("sendMessage", {"chat_id": chat_id, "text": text})


def handle(update):
    message = update.get("message") or {}
    text = message.get("text")
    chat = message.get("chat") or {}
    if not text or "id" not in chat:
        return
    if text.startswith("/start"):
        name = (message.get("from") or {}).get("first_name") or "دوست من"
        reply(chat["id"], START_TEXT.format(name=name))
    else:
        reply(chat["id"], text)


def poll():
    offset = None
    while True:
        try:
            if not state["ok"]:
                me = call("getMe", timeout=15)
                state.update(ok=True, username=me.get("username"))
                # Long polling and a webhook can't both be active.
                call("deleteWebhook", timeout=15)
                print(f"bot @{state['username']} is up", flush=True)
            params = {"timeout": 30, "allowed_updates": ["message"]}
            if offset is not None:
                params["offset"] = offset
            for update in call("getUpdates", params, timeout=40):
                offset = update["update_id"] + 1
                try:
                    handle(update)
                except Exception as error:  # one bad update must not stop the bot
                    print(f"update {update.get('update_id')} failed: {error}", flush=True)
        except urllib.error.HTTPError as error:
            if error.code == 401:
                print("TELEGRAM_BOT_TOKEN was rejected by Telegram (401). Fix it in env vars and restart.", flush=True)
                state["ok"] = False
                time.sleep(60)
                continue
            print(f"telegram http error {error.code}, retrying", flush=True)
            time.sleep(5)
        except Exception as error:
            print(f"telegram error: {error}, retrying", flush=True)
            time.sleep(5)


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/health", "/"):
            body = json.dumps({"status": "ok", "bot": state["username"], "telegram": state["ok"]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


def main():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN is not set.", file=sys.stderr, flush=True)
    else:
        threading.Thread(target=poll, daemon=True).start()
    print(f"health on :{PORT}/health", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Health).serve_forever()


if __name__ == "__main__":
    main()

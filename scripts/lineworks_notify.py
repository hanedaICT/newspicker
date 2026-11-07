
"""LINE WORKS Bot通知用モジュール。"""

import json
import os
import time
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import jwt


TOKEN_URL = "https://auth.worksmobile.com/oauth2/v2.0/token"
API_BASE = "https://www.worksapis.com/v1.0"


def send_lineworks_message(message: str) -> bool:
    """メッセージを送信する。失敗時はFalseを返す。"""
    try:
        names = (
            "LINEWORKS_CLIENT_ID",
            "LINEWORKS_CLIENT_SECRET",
            "LINEWORKS_SERVICE_ACCOUNT",
            "LINEWORKS_PRIVATE_KEY",
            "LINEWORKS_BOT_ID",
            "LINEWORKS_RECIPIENT_ID",
        )

        config = {name: os.environ.get(name, "") for name in names}
        missing = [name for name, value in config.items() if not value]

        if missing:
            print(f"[LINEWORKS] 設定不足: {', '.join(missing)}")
            return False

        client_id = config["LINEWORKS_CLIENT_ID"]
        now = int(time.time())

        claims = {
            "iss": client_id,
            "sub": config["LINEWORKS_SERVICE_ACCOUNT"],
            "iat": now,
            "exp": now + 3600,
        }

        private_key = config["LINEWORKS_PRIVATE_KEY"].replace(
            "\\n", "\n"
        )

        assertion = jwt.encode(
            claims,
            private_key,
            algorithm="RS256",
            headers={"typ": "JWT"},
        )

        token_data = urlencode({
            "assertion": assertion,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": client_id,
            "client_secret": config["LINEWORKS_CLIENT_SECRET"],
            "scope": "bot.message",
        }).encode("utf-8")

        token_request = Request(
            TOKEN_URL,
            data=token_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            method="POST",
        )

        with urlopen(token_request, timeout=15) as response:
            token = json.load(response)["access_token"]

        bot_id = quote(config["LINEWORKS_BOT_ID"], safe="")
        recipient_id = quote(
            config["LINEWORKS_RECIPIENT_ID"], safe=""
        )

        url = (
            f"{API_BASE}/bots/{bot_id}"
            f"/users/{recipient_id}/messages"
        )

        payload = json.dumps({
            "content": {
                "type": "text",
                "text": message[:2000],
            }
        }, ensure_ascii=False).encode("utf-8")

        message_request = Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(message_request, timeout=15) as response:
            if response.status != 201:
                print("[LINEWORKS] 通知失敗")
                return False

        print("[LINEWORKS] 通知送信成功")
        return True

    except Exception as exc:
        # トークンや秘密鍵などの機密情報はログに出さない
        print(f"[LINEWORKS] 通知失敗: {type(exc).__name__}")
        return False

import os
from pathlib import Path
import json
import urllib.request

# 仅在本地开发时加载 .env；线上（Lambda）没有 .env 也不会报错
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except Exception:
    # 没装 python-dotenv 或没找到 .env 时忽略
    pass

default_webhook  = os.getenv("TEAMS_WEBHOOK")

def send_table_as_text(table_text: str, webhook: str | None = None, timeout_sec: int = 20):
    url = (webhook or default_webhook).strip()
    payload = {
        "text": f"📊 最近 7 天邮件发送统计\n```\n{table_text}\n```"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        return resp.status, resp.read().decode()
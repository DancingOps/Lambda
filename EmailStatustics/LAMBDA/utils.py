import os
from pathlib import Path
import base64
import json
import urllib.parse
import urllib.request
import datetime

# 仅在本地开发时加载 .env；线上（Lambda）没有 .env 也不会报错
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except Exception:
    # 没装 python-dotenv 或没找到 .env 时忽略
    pass

# 统一用 os.environ 取值（本地来自 .env，线上来自 Lambda 环境变量/参数服务）
#print(os.getenv("TIME_ZONE"))
# ==== 基础配置（保持你当前的简单写法）====
time_zone    = os.getenv("ENGAGELAB_TIME_ZONE")
aggregate_by = os.getenv("ENGAGELAB_AGGREGATE_BY")
api_users    = os.getenv("ENGAGELAB_USERS")
username     = os.getenv("ENGAGELAB_API_USER")
password     = os.getenv("ENGAGELAB_API_KEY")
base_url     = os.getenv("ENGAGELAB_BASE_URL")

# ==== Basic Auth ====
token = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {token}"}

# ==== 格式化 ====
def format_int(num):
    try:
        return f"{int(num):,}"
    except Exception:
        return str(num)

def format_percent(p):
    # 接口已返回数字百分比（如 0.89 或 99.11），这里只负责加 %
    return "N/A" if p is None else f"{p}%"

# ==== 拉取单日（直接使用接口返回字段名）====
def fetch_one_day(day: str) -> dict:
    """
    start_date=end_date=day，返回：
    {
      "date": "...",
      "targets": ...,
      "delivered": ..., "delivered_percent": ...,
      "invalid_email": ..., "invalid_email_percent": ...,
      "soft_bounce": ..., "soft_bounce_percent": ...,
      "billing_count": ...
    }
    """
    params = {
        "time_zone": time_zone,
        "aggregate_by": aggregate_by,
        "api_users": api_users,
        "start_date": day,
        "end_date": day,
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode()
        data = json.loads(body)

    # 按你提供的真实返回结构：{"result": {...一堆字段...}}
    result = data.get("result", {}) or {}

    return {
        "date": day,
        "targets": result.get("targets", 0),
        "delivered": result.get("delivered", 0),
        "delivered_percent": result.get("delivered_percent"),
        "invalid_email": result.get("invalid_email", 0),
        "invalid_email_percent": result.get("invalid_email_percent"),
        "soft_bounce": result.get("soft_bounce", 0),
        "soft_bounce_percent": result.get("soft_bounce_percent"),
        "billing_count": result.get("billing_count", 0),
    }

# ==== 最近 7 天（不含当天）====
def fetch_last_7_days_rows():
    today = datetime.date.today()
    # 昨天开始往前 6 天，共 7 天；升序
    date_list = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
    date_list.sort()
    rows = []
    for day in date_list:
        try:
            rows.append(fetch_one_day(day))
        except Exception:
            rows.append({
                "date": day,
                "targets": 0,
                "delivered": 0, "delivered_percent": None,
                "invalid_email": 0, "invalid_email_percent": None,
                "soft_bounce": 0, "soft_bounce_percent": None,
                "billing_count": 0
            })
    return rows

# ==== 打印 ASCII 表格（数量 与 百分比同一单元格）====
# 放在 utils.py 里（保留你现有的 format_int/format_percent）

def render_table(rows):
    header = ["Date", "Target", "Delivered", "Invalid Email", "Soft Bounce", "Billing Count"]
    lines = []
    lines.append(f"{header[0]:<12} | {header[1]:>10} | {header[2]:>18} | {header[3]:>16} | {header[4]:>12} | {header[5]:>13}")
    lines.append("-" * 100)
    for r in rows:
        delivered = f"{format_int(r['delivered'])} ({format_percent(r['delivered_percent'])})"
        invalid   = f"{format_int(r['invalid_email'])} ({format_percent(r['invalid_email_percent'])})"
        soft      = f"{format_int(r['soft_bounce'])} ({format_percent(r['soft_bounce_percent'])})"
        lines.append(f"{r['date']:<12} | {format_int(r['targets']):>10} | {delivered:>18} | {invalid:>16} | {soft:>12} | {format_int(r['billing_count']):>13}")
    return "\n".join(lines)

def print_table(rows, return_str: bool = False):
    s = render_table(rows)
    if return_str:
        return s
    print(s)

# ==== 本地调试入口 ====
if __name__ == "__main__":
    rows = fetch_last_7_days_rows()
    print_table(rows)
    


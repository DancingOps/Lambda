from utils import fetch_last_7_days_rows, print_table
from teams_sender import send_table_as_text

def lambda_handler(event=None, context=None):
    # 1) 拉数据
    rows = fetch_last_7_days_rows()

    # 2) 生成 ASCII 表格字符串（同时你也可以 print 一份到日志）
    table_text = print_table(rows, return_str=True)

    # 3) 发送到 Teams（使用 teams_sender.py 中写死的 DEFAULT_WEBHOOK）
    status, body = send_table_as_text(table_text)

    return {"ok": status == 200, "status": status, "body": body}

if __name__ == "__main__":
    res = lambda_handler()
    print(res)
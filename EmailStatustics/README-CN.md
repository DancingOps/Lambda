# Lambda-EmailStatistics
## 基础功能

​	调用Engagelab邮件接口，使用teams Incoming Webhook作为连接器，发送最近7天的 Engagelab 邮件统计结果到teams频道。

## 输出样式

| Date       | Target | Delivered      | Invalid Email | Soft Bounce | Billing Count |
|-------------|---------|----------------|----------------|--------------|----------------|
| 2025-10-06 | 1,369 | 1,359 (99.27%) | 10 (0.73%) | 0 (0.0%) | 1,366 |
| 2025-10-07 | 1,551 | 1,531 (98.71%) | 20 (1.29%) | 0 (0.0%) | 1,547 |
| 2025-10-08 | 3,301 | 3,292 (99.73%) | 9 (0.27%) | 0 (0.0%) | 3,301 |
| 2025-10-09 | 2,349 | 2,334 (99.36%) | 15 (0.64%) | 0 (0.0%) | 2,346 |
| 2025-10-10 | 2,125 | 2,116 (99.58%) | 9 (0.42%) | 0 (0.0%) | 2,124 |
| 2025-10-11 | 2,888 | 2,871 (99.41%) | 17 (0.59%) | 0 (0.0%) | 2,882 |
| 2025-10-12 | 1,724 | 1,707 (99.01%) | 17 (0.99%) | 0 (0.0%) | 1,712 |

## 配置方式

​	可以采用两种方式配置。环境变量多用于在AWS提供的SAAS环境中，配置文件多用于本地主机运行。同时配置时，只有配置文件生效。

### 环境变量

| 变量名                 | 示例值                                        | 备注                                                         |
| ---------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| ENGAGELAB_USERS        | "user1;user2;user3;user4;user5"               | 邮件统计目标用户（收件人分组或业务标识）                     |
| ENGAGELAB_API_USER     | "username"                                    | EngageLab 平台的 API 用户名                                  |
| ENGAGELAB_API_KEY      | "password"                                    | EngageLab 平台的 API 密钥，用于身份认证                      |
| ENGAGELAB_BASE_URL     | "https://email.api.engagelab.cc/v1/stats_day" | EngageLab 邮件统计 API 地址                                  |
| ENGAGELAB_TIME_ZONE    | "+8"                                          | 时区设置                                                     |
| ENGAGELAB_AGGREGATE_BY | "1"                                           | 数据聚合粒度（1=按日统计）                                   |
| TEAMS_WEBHOOK          | ""                                            | Microsoft Teams 群组机器人 Incoming Webhook 地址，用于发送统计结果 |

###  配置文件

​	在 README.md 同级别目录创建.env文件。

```
ENGAGELAB_USERS="user1;user2;user3;user4;user5"
ENGAGELAB_API_USER="username"
ENGAGELAB_API_KEY="password"
ENGAGELAB_BASE_URL = "https://email.api.engagelab.cc/v1/stats_day"
ENGAGELAB_TIME_ZONE = "+8"
ENGAGELAB_AGGREGATE_BY = "1"
TEAMS_WEBHOOK=https://novaxteam.webhook.office.com/webhookb2/····
```

## 运行方式

```python
python3 -m venv .venv
source .venv/bin/activate.fish 
pip3.13 install -r requirements.txt

# 使用vscode打开此EmailStatistics目录（让vscode识别venu）
python3.13 LAMBDA/utils.py # 查看Engagelab邮件统计表格是否正确
python3.13 LAMBDA/lamdba_function.py
```
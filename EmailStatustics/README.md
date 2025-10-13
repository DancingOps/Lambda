# Lambda-EmailStatistics
## Basic Functions

​	Invoke the Engagelab email interface, using the teams Incoming Webhook as a connector, to send the Engagelab email statistics for the past 7 days to the teams channel.

## Output Style

| Date       | Target | Delivered      | Invalid Email | Soft Bounce | Billing Count |
|-------------|---------|----------------|----------------|--------------|----------------|
| 2025-10-06 | 1,369 | 1,359 (99.27%) | 10 (0.73%) | 0 (0.0%) | 1,366 |
| 2025-10-07 | 1,551 | 1,531 (98.71%) | 20 (1.29%) | 0 (0.0%) | 1,547 |
| 2025-10-08 | 3,301 | 3,292 (99.73%) | 9 (0.27%) | 0 (0.0%) | 3,301 |
| 2025-10-09 | 2,349 | 2,334 (99.36%) | 15 (0.64%) | 0 (0.0%) | 2,346 |
| 2025-10-10 | 2,125 | 2,116 (99.58%) | 9 (0.42%) | 0 (0.0%) | 2,124 |
| 2025-10-11 | 2,888 | 2,871 (99.41%) | 17 (0.59%) | 0 (0.0%) | 2,882 |
| 2025-10-12 | 1,724 | 1,707 (99.01%) | 17 (0.99%) | 0 (0.0%) | 1,712 |

## Configuration method

​	Two methods can be used for configuration. Environment variables are mostly used in the AWS-provided SAAS environment, while configuration files are mostly used for local host operation. When configured simultaneously, only the configuration file takes effect.

### Environmental variable

| Variable name          | Example value                                 | Note                                                         |
| ---------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| ENGAGELAB_USERS        | "user1;user2;user3;user4;user5"               | Email statistics target user (recipient group or business identifier) |
| ENGAGELAB_API_USER     | "username"                                    | EngageLab platform API username                              |
| ENGAGELAB_API_KEY      | "password"                                    | API key for EngageLab platform, used for identity authentication |
| ENGAGELAB_BASE_URL     | "https://email.api.engagelab.cc/v1/stats_day" | EngageLab email statistics API address                       |
| ENGAGELAB_TIME_ZONE    | "+8"                                          | Time zone setting                                            |
| ENGAGELAB_AGGREGATE_BY | "1"                                           | Data Aggregation Granularity (1=Daily Statistics)            |
| TEAMS_WEBHOOK          | ""                                            | Microsoft Teams group robot incoming webhook address, used to send statistical results |

###  Configuration file

​	Create a .env file in the same level directory as README.md.

```
ENGAGELAB_USERS="user1;user2;user3;user4;user5"
ENGAGELAB_API_USER="username"
ENGAGELAB_API_KEY="password"
ENGAGELAB_BASE_URL = "https://email.api.engagelab.cc/v1/stats_day"
ENGAGELAB_TIME_ZONE = "+8"
ENGAGELAB_AGGREGATE_BY = "1"
TEAMS_WEBHOOK=https://novaxteam.webhook.office.com/webhookb2/····
```

## Operation mode

```python
python3 -m venv .venv
source .venv/bin/activate.fish 
pip3.13 install -r requirements.txt

# Open this EmailStatistics directory with vscode (let vscode recognize venu)
python3.13 LAMBDA/utils.py # Check if the Engagelab email statistics table is correct.
python3.13 LAMBDA/lamdba_function.py
```
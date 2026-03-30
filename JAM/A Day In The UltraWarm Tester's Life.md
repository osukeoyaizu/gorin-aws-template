## task1
OpenSearchのセキュリティ設定のaws:SourceIpをローカルPCのグローバルIPに変更して回答する

## task2,3
「ダッシュボード」→「Index Management」→「State management policies」
### ism-policy-jam-ultrawarm-issueを編集
```
{
    "policy": {
        "policy_id": "ism-policy-jam-ultrawarm-issue",
        "description": "Run a hot-warm-delete workflow.",
        "last_updated_time": 1760508183603,
        "schema_version": 13,
        "error_notification": null,
        "default_state": "hot_state",
        "states": [
            {
                "name": "hot_state",
                "actions": [],
                "transitions": [
                    {
                        "state_name": "warm_state",
                        "conditions": {
                            "min_index_age": "7d"
                        }
                    }
                ]
            },
            {
                "name": "warm_state",
                "actions": [
                    {
                        "timeout": "24h",
                        "retry": {
                            "count": 5,
                            "backoff": "exponential",
                            "delay": "1h"
                        },
                        "warm_migration": {}
                    }
                ],
                "transitions": []
            }
        ],
        "ism_template": [
            {
                "index_patterns": [
                    "cwl-*"
                ],
                "priority": 0,
                "last_updated_time": 1760508183603
            }
        ]
    }
}
```

## task4
ism-policy-jam-ultrawarm-issueを削除する

「ダッシュボード」→「Dev Tools」
```
DELETE cwl-*
```

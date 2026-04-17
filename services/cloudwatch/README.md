## CloudWatch Agentをインストール
https://qiita.com/sugimount-a/items/4f332e4128984a1b3b7d

### 必要なポリシー
CloudWatchAgentServerPolicy

### インストール
```
sudo yum install -y amazon-cloudwatch-agent
```

### collectdインストール
```
sudo yum install -y collectd
```

### wizard起動
```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

### 実行
```
cd /opt/aws/amazon-cloudwatch-agent/bin/
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:config.json
```


### プロセス監視(nginx)
- config.jsonのメトリクスにprocstatを追加
```
                "metrics_collected": {
                        "collectd": {
                                "metrics_aggregation_interval": 60
                        },
                        "disk": {
                                "measurement": [
                                        "used_percent"
                                ],
                                "metrics_collection_interval": 60,
                                "resources": [
                                        "*"
                                ]
                        },
                        "mem": {
                                "measurement": [
                                        "mem_used_percent"
                                ],
                                "metrics_collection_interval": 60
                        },
                        "statsd": {
                                "metrics_aggregation_interval": 60,
                                "metrics_collection_interval": 10,
                                "service_address": ":8125"
                        },
                        "procstat": [
                                {
                                        "pattern": "/usr/sbin/nginx",
                                        "pid_finder": "pgrep",
                                        "measurement": [
                                                "pid_count"
                                        ],
                                        "metrics_collection_interval": 60
                                }
                        ]
                }
```


## ログに出力される特定の値をマスキングする
### ロググループのアクションからデータ保護ポリシーを作成する
例:メールアドレスをマスクする → マネージドデータ識別子のEmailAddressを選択する

**※正規表現を使用したマスキングも可能**

## CloudWatch Logs Insights
https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html
### @messageに文字列「error」が含まれるログを、タイムスタンプの順に20件取得する
```
fields @timestamp, @message
| filter @message like /error/
| sort @timestamp
| limit 20
```

### parse
*? は「最短一致」なので、次に来る区切り（スペースや次のパターン）までで止まる

endpointが /api/v1/users/12345 の場合→/api/v1/users
```
fields @timestamp, endpoint

| parse endpoint '*?' as endpointbase
```


## メトリクスフィルター
### VPCフローログの通信拒否のログを検知するフィルターパータン
```
[version, account, eni, source, destination, srcport, destport, protocol,packets, bytes, windowstart, windowend, action="REJECT", flowlogstatus]
```

## RUN
ドメインリスト:アプリケーションのDNSを入力

カスタムイベントにチェックをつける

新しいIDプールを作成するを選択

サンプルコードでHTMLを選択し、scriptタグ内容をコピーし、.jsファイルを作成する

S3に.jsファイルをアップロードし、CloudFrontで公開する

### アプリケーションのコード例
- ...cwrum.jsでSDKを読み込み

    - CloudWatch RUMのクライアントライブラリをブラウザにロード

    - このライブラリは cwr() という関数を提供

- cwr('init', {...})で初期化

    - App Monitor ID、Cognito IDプール、リージョン、計測対象（performance, errors, http）などを設定

    - RUMがページロードやHTTPリクエストを監視できる状態になる

- recordLatency()関数

    - ボタンを押すと、ランダムなレイテンシ値を生成

    - cwr('recordEvent', {...})でカスタムイベントをキューに追加

    - cwr('dispatch')でCloudWatchに送信
```
<!DOCTYPE html>
<html>
  <head>
    <script type='text/javascript' src='http://d294ydithl1m43.cloudfront.net/cwrum.js'></script>
  </head>
<body>
    <h2>CloudWatch RUM Minimal Example</h2>
    <button onclick="recordLatency()">Record Latency Event</button>

    <script>
        // ページロード時にRUM初期化（通常はAWSコンソールで生成した設定を追加）
        cwr('init', {
            sessionSampleRate: 1, // 全セッション記録
            identityPoolId: 'YOUR_IDENTITY_POOL_ID', // Cognito IDプール
            endpoint: 'https://dataplane.rum.us-east-1.amazonaws.com',
            telemetries: ['performance', 'errors', 'http'],
            allowCookies: true,
            enableXRay: false
        });

        // カスタムイベント記録の例
        function recordLatency() {
            const latency = Math.random() * 1000; // ダミー値
            cwr('recordEvent', {
                type: 'latencyMeasurement',
                data: {
                    functionName: 'TestFunction',
                    latency: latency.toFixed(2),
                    timestamp: new Date().toISOString()
                }
            });
            cwr('dispatch'); // イベント送信
            alert('Latency event recorded: ' + latency.toFixed(2) + ' ms');
        }
    </script>
</body>
</html>
```


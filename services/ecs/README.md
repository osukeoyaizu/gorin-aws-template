## Blue/Greenデプロイ

### 前提条件
#### ECSのIAMロール
AmazonEC2ContainerServiceRole

lambda:*

#### タスクのIAMロール
AmazonECSTaskExecutionRolePolicy

CloudWatchAgentServerPolicy


### デプロイライフサイクルフック(Lambda)
※約5分間本番とテスト環境が存在するコード
```
import json
import time
def lambda_handler(event, context):
    print(f"{json.dumps(event)}")
    print(event['lifecycleStage'])
    if event['lifecycleStage'] == 'TEST_TRAFFIC_SHIFT':
        print('wait 5 minutes')
        time.sleep(300)
    return {
        'hookStatus': 'SUCCEEDED'
        #'hookStatus': 'FAILED'
    }
```

### 本番環境へのアクセス
curl https://xxxxxyyyy.cloudfront.net

{"message": "prod"}

### 開発環境へのアクセス

curl -H "x-amzn-ecs-blue-green-test: test" https://xxxxxyyyy.cloudfront.net/

{"message": "dev"}


## Service Connect(nginxのリバースプロキシ)
### flask
#### サービスの設定
Service Connectの設定:クライアントとサーバー

名前空間:Cloud MapでAPI呼び出しで作成した名前空間

ポートエイリアス:flask-8080-tcp

検出:flask-8080-tcp

DNS:flask-8080-tcp

ポート:8080

セキュリティグループでnginxタスクからのアクセス許可

#### app/main.py
```
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'result':'OK'}), 200

@app.route('/health', methods=['GET'])
def health():
    return "Hello, world!"

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8080, threaded=True)
```

#### Dockerfile
```
FROM amazonlinux:2023

EXPOSE 8080

COPY ./app /app

WORKDIR /app

RUN yum install python pip -y

RUN pip install flask

CMD python /app/main.py
```

### nginx
#### サービスの設定
Service Connectの設定:クライアント側のみ

名前空間:flask側と同じ名前空間

ロードバランシング

セキュリティグループでALBからのアクセス許可

#### nginx.conf
```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log notice;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
          proxy_http_version 1.1;
          proxy_pass http://flask-8080-tcp:8080/;
        }


        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }
}
```
#### Dockerfile
```
FROM amazonlinux:2023

RUN yum install -y nginx

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
```

## タスク定義
特定のインスタンスタイプでのみ配置したい場合
- タスク配置
    - タイプ:memberOf
    - 式:attribute.ecs.instance-type == <インスタンスタイプ>
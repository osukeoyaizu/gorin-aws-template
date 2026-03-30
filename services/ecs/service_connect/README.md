## ALBのルールを使用するパターン
クライアントからのアクセス /service01

アプリケーションも/service01で待ち受けている

### flaskの例
@app.route('/service01', methods=['GET'])

### nginx.conf
```
        location /service01 {
          proxy_http_version 1.1;
          proxy_pass http://{サービスコネクトのDNS}:{ポート}/service01;
        }
```


## Service Connectを使用するパターン
クライアントからのアクセス /service01

アプリケーションのは/で待ち受けている

### flaskの例
@app.route('/', methods=['GET'])


### nginx.conf
```
        location /service01 {
          proxy_http_version 1.1;
          proxy_pass http://{サービスコネクトのDNS}:{ポート}/;
        }
```

### クライアントからのアクセスが/service01/の場合のnginx.conf
```
        location /service01/ {
          proxy_http_version 1.1;
          proxy_pass http://{サービスコネクトのDNS}:{ポート}/;
        }
```

## Federated Queries
### S3
#### 事前準備
クローラーでデータカタログを作成しておく

lakeformationを使用している場合はIAMロールに権限を与えておく

IAMロールにポリシーをアタッチ(AmazonS3FullAccess,AWSGlueConsoleFullAccess,kms)

#### 外部スキーマ作成
```
create external schema <作成する外部スキーマ名> 
from data catalog 
database '<データベース名>'
iam_role '<RedshiftのロールARN>';
```

### PostgreSQL
#### 事前準備
RDSのセキュリティグループでRedshiftのノードIPアドレスを許可する

IAMロールにポリシーをアタッチ(SecretsManagerReadWrite,kms)

RDSのパラメータグループのpassword_encryptionをmd5に変更する(※変更後に再起動が必要)

postgresqlで以下のクエリ実行
```
set password_encryption = 'md5';
alter user postgres with password '<パスワード>';
```

#### 外部スキーマ作成
```
CREATE EXTERNAL SCHEMA <作成する外部スキーマ名>
FROM POSTGRES
DATABASE '<接続先データベース>'
SCHEMA '<接続先スキーマ>'
URI '<RDSのエンドポイント>'
PORT 5432
IAM_ROLE '<RedshiftのロールARN>'
SECRET_ARN '<SecretsManagerのARN>';
```
```
SELECT * FROM <外部スキーマ>.<テーブル名> LIMIT 10;
```

### MySQL
#### 事前準備
RDSのセキュリティグループでRedshiftのノードIPアドレスを許可する

IAMロールにポリシーをアタッチ(SecretsManagerReadWrite,kms)

#### 外部スキーマ作成
```
CREATE EXTERNAL SCHEMA <作成する外部スキーマ名>
FROM MYSQL
DATABASE '<接続先データベース>'
URI '<RDSのエンドポイント>'
PORT 3306
IAM_ROLE '<RedshiftのロールARN>'
SECRET_ARN '<SecretsManagerのARN>';
```



## S3のデータをロード
### CSV
```
COPY {テーブル名} 
FROM 's3://{バケット名}/{ファイル名}'
iam_role '{IAMロールのARN}'
FORMAT AS CSV
IGNOREHEADER 1
NULL 'NaN'
DATEFORMAT 'auto'
TIMEFORMAT 'DD/MM/YYYY HH:MI:SS';
```

### JSON
```
COPY public.user_purchases
FROM 's3://{バケット名}/{ファイル名}'
IAM_ROLE '{IAMロールのARN}'
FORMAT AS JSON 'auto'
TIMEFORMAT 'auto'
```

### エラーログ確認
```
select * from sys_load_error_detail;
```

## クエリ
### ユーザー作成
```
CREATE USER {ユーザー名} WITH PASSWORD '{パスワード}';
```

### ROLE作成
```
CREATE ROLE {ROLE名};
```

### ユーザーにROLE付与
```
GRANT ROLE {ROLE名} TO {ユーザー名};
```

### ユーザーの切り替え
```
SET  SESSION AUTHORIZATION {ユーザー名}
```

### 列レベルのセキュリティ
```
GRANT SELECT({列1},{列2}) ON {テーブル名} TO ROLE {ROLE名};
```

### 行レベルのセキュリティ
#### ポリシー作成
```
CREATE RLS POLICY {ポリシー名} WITH ( {列名} BOOLEAN ) USING ( {列名} = true )
```
#### ポリシーアタッチ
```
ATTACH RLS POLICY {ポリシー名}
ON {テーブル名}
TO ROLE {ROLE名};
```
#### テーブルでRLSをオンにする
```
ALTER TABLE {テーブル名} ROW LEVEL SECURITY on;
```

### マスキング
#### マスキングポリシー作成
「phone」カラムをXXXXに置き換える
```
CREATE MASKING POLICY mask_phone WITH (phone VARCHAR(256)) USING ('XXXX'::TEXT);
```

#### マスキングポリシーをロールにアタッチ
「customer_table」の「phone」カラムに「mask_phone」ポリシーを適用

適用対象は「analytics_role」
```
ATTACH MASKING POLICY mask_phone ON customer_table(phone) TO ROLE analytics_role;
```

### データ共有
**コンソール上でできる**
#### データ共有を作成(プロデューサー側)
```
CREATE DATASHARE my_datashare SET PUBLICACCESSIBLE TRUE;
```

#### スキーマやテーブルを共有対象に追加(プロデューサー側)
```
ALTER DATASHARE my_datashare ADD SCHEMA my_schema;
ALTER DATASHARE my_datashare ADD TABLE my_schema.my_table;
```

#### コンシューマーに使用権限を付与(プロデューサー側)
```
GRANT USAGE ON DATASHARE my_datashare TO NAMESPACE 'consumer-namespace-id';
```

#### データ共有を参照(コンシューマー側)
```
SHOW DATASHARES
```

#### データ共有をデータベースにアタッチ(コンシューマー側)
※読み取り専用
```
CREATE DATABASE shared_db 
FROM DATASHARE my_datashare OF NAMESPACE 'producer-namespace-id';
```

#### データ共有を書き込み許可
プロデューサー側
```
GRANT ALL ON TABLE my_schema.my_table TO DATASHARE my_datashare;
```
コンシューマー側
```
CREATE DATABASE shared_db
WITH PERMISSIONS
FROM DATASHARE my_datashare OF NAMESPACE 'producer-namespace-id';
```
```
create user <ユーザー名> password '<パスワード>';
SET SESSION AUTHORIZATION '<ユーザー名>'
GRANT ALL ON DATABASE shared_db TO <ユーザー名>;
GRANT ALL ON SCHEMA shared_db.my_schema TO <ユーザー名>;
GRANT ALL ON ALL TABLES IN SCHEMA shared_db.my_schema TO <ユーザー名>;
```

#### 共有データを利用(コンシューマー側)
```
SELECT * FROM shared_db.my_schema.my_table;
```

## ビュー
### ビュー作成
```
CREATE MATERIALIZED VIEW nation_region_view
AUTO REFRESH YES AS
SELECT
* 
FROM table_a AS A
INNER JOIN table_b AS B 
ON A.key = B.a_key;
```


## IAM認証
```
CREATE USER "IAMR:{ロール名}" WITH PASSWORD DISABLE;
GRANT USAGE ON SCHEMA public TO "IAMR:{ロール名}";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "IAMR:{ロール名}";
```

## Redshift ML
### ネットワークログから攻撃種別（label）を予測するための機械学習モデル
#### トレーニングテーブル
```
CREATE TABLE network_logs_train (
    session_id BIGINT,
    src_ip VARCHAR(50),
    dst_ip VARCHAR(50),
    packet_size INT,
    http_method VARCHAR(10),
    response_code INT,
    label INT  -- 攻撃種別（0～4）
);
```
#### トレーニングテーブルにデータ登録
```
INSERT INTO network_logs_train
SELECT
    seq AS session_id,
    '192.168.' || (seq % 255) || '.' || (seq % 100) AS src_ip,
    '10.0.' || (seq % 255) || '.' || (seq % 100) AS dst_ip,
    (seq % 1500) + 100 AS packet_size,
    CASE (seq % 4)
        WHEN 0 THEN 'GET'
        WHEN 1 THEN 'POST'
        WHEN 2 THEN 'PUT'
        ELSE 'DELETE'
    END AS http_method,
    CASE (seq % 5)
        WHEN 0 THEN 200
        WHEN 1 THEN 404
        WHEN 2 THEN 500
        WHEN 3 THEN 403
        ELSE 301
    END AS response_code,
    (seq % 5) AS label
FROM (
    SELECT (a.n + b.n * 10) AS seq
    FROM (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
         (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 UNION ALL SELECT 31 UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35 UNION ALL SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40 UNION ALL SELECT 41 UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50 UNION ALL SELECT 51 UNION ALL SELECT 52 UNION ALL SELECT 53 UNION ALL SELECT 54 UNION ALL SELECT 55 UNION ALL SELECT 56 UNION ALL SELECT 57 UNION ALL SELECT 58 UNION ALL SELECT 59 UNION ALL SELECT 60 UNION ALL SELECT 61 UNION ALL SELECT 62 UNION ALL SELECT 63 UNION ALL SELECT 64 UNION ALL SELECT 65 UNION ALL SELECT 66 UNION ALL SELECT 67 UNION ALL SELECT 68 UNION ALL SELECT 69 UNION ALL SELECT 70 UNION ALL SELECT 71 UNION ALL SELECT 72 UNION ALL SELECT 73 UNION ALL SELECT 74 UNION ALL SELECT 75 UNION ALL SELECT 76 UNION ALL SELECT 77 UNION ALL SELECT 78 UNION ALL SELECT 79 UNION ALL SELECT 80 UNION ALL SELECT 81 UNION ALL SELECT 82 UNION ALL SELECT 83 UNION ALL SELECT 84 UNION ALL SELECT 85 UNION ALL SELECT 86 UNION ALL SELECT 87 UNION ALL SELECT 88 UNION ALL SELECT 89 UNION ALL SELECT 90 UNION ALL SELECT 91 UNION ALL SELECT 92 UNION ALL SELECT 93 UNION ALL SELECT 94 UNION ALL SELECT 95 UNION ALL SELECT 96 UNION ALL SELECT 97 UNION ALL SELECT 98 UNION ALL SELECT 99) b
) t
WHERE seq BETWEEN 1 AND 1000;
```

#### 推論用テーブル(ラベルなしのカラム)
```
CREATE TABLE network_logs_test (
    session_id BIGINT,
    src_ip VARCHAR(50),
    dst_ip VARCHAR(50),
    packet_size INT,
    http_method VARCHAR(10),
    response_code INT
);
```
#### 推論用テーブルにデータ登録
```
INSERT INTO network_logs_test VALUES
(101, '192.168.2.1', '10.0.1.1', 600, 'GET', 200),
(102, '192.168.2.2', '10.0.1.2', 900, 'POST', 404),
(103, '192.168.2.3', '10.0.1.3', 300, 'GET', 500),
(104, '192.168.2.4', '10.0.1.4', 700, 'PUT', 403),
(105, '192.168.2.5', '10.0.1.5', 150, 'DELETE', 200);
```
#### モデル作成
- Target列の型はINTやFLOATにする(SELECT内の例:CAST(<ターゲット列> AS FLOAT8))
- PROBLEM_TYPE を指定しないといけない場合がある
    - 回帰: REGRESSION
    - 二値分類: BINARY_CLASSIFICATION
```
CREATE MODEL predict_web_attacks
FROM (
    SELECT
        src_ip,
        dst_ip,
        packet_size,
        http_method,
        response_code,
        label
    FROM network_logs_train
)
TARGET label
FUNCTION predict_web_attacks
IAM_ROLE DEFAULT
SETTINGS (
    S3_BUCKET '<S3バケット>',
    MAX_RUNTIME 1500
)
```
#### モデルの状態やメタ情報を確認
※Model StateがREADYになったら使用可能
```
SHOW MODEL predict_web_attacks;
```

#### 推論クエリ
```
SELECT
    session_id,
    predict_web_attacks(src_ip, dst_ip, packet_size, http_method, response_code) AS predicted_label
FROM network_logs_test;

```

### Bedrockとの統合
目標:患者一人ひとりの病状に基づいたパーソナライズされた食事プランを提供する
#### サンプルデータ(mv_prompts)
```
102	Ema has Hypertension,Bronchitis taking Clevidipine,Naproxen	
105	Deb has Prediabetes,Viral sinusitis taking Metformin,fluticasone	
101	John has Asthma,Hypothyroidism taking Fluticasone,Levothroxine	
103	Ken has Muscle strain taking Morphine	
104	Zen has Viral sinusitis,Bronchitis taking Budesonide,Naproxen	
```

#### Bedrock上のLLMモデルを参照するモデルを作成
```
CREATE EXTERNAL MODEL patient_recommendations
FUNCTION patient_recommendations_func
IAM_ROLE DEFAULT
MODEL_TYPE BEDROCK
SETTINGS (
    MODEL_ID 'amazon.nova-lite-v1:0',
    PROMPT 'Generate personalized diet plan for following patient:');
```

#### 関数にプロンプトを渡す
```
SELECT patient_recommendations_func(patient_prompt) 
FROM mv_prompts limit 2;
```
※アカウント設定から「Allow export result set」を有効化しておくことで結果をダウンロードできる

## S3 event integrations
### S3バケットのバケットポリシー
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Auto-Copy-Policy-01",
            "Effect": "Allow",
            "Principal": {
                "Service": "redshift.amazonaws.com"
                },
            "Action": [
                "s3:GetBucketNotification",
                "s3:PutBucketNotification",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::<S3 Bucket Name>",
            "Condition": {
                "StringLike": {
                    "aws:SourceArn": "arn:aws:redshift:<AWS Region>:<AWS Account Number>:integration:*", 
                    "aws:SourceAccount": "<AWS Account Number>" 
                }
            }
        }
    ]
}
```

### Redshift Serverless NamaSpaceのリソースポリシー
承認されたプリンシパル・・・アカウントID

承認された統合リソース・・・S3バケットのARN


### S3 event integrations作成
ソースにS3バケットを選択

TargetにRedshift Serverlessを選択

以下のデータ(CSV)をS3に保存
```
id,name,email,signup_date
1,Alice Johnson,alice@example.com,2023-01-15
2,Bob Smith,bob@example.com,2023-02-20
3,Charlie Brown,charlie@example.com,2023-03-05
```

### クエリエディタv2でクエリ
#### テーブル作成
```
CREATE TABLE public.{テーブル名} (
    id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    signup_date DATE
);
```

#### コピージョブ作成
```
COPY public.{テーブル名}
FROM 's3://{S3バケット}'
IAM_ROLE '{IAMロールARN}'
REGION '{リージョン}'
DELIMITER ','
IGNOREHEADER 1
JOB CREATE {ジョブ名}
AUTO ON;
```

### 確認
S3にファイルをアップロードする → しばらく待ってSELECTするとデータが反映されている

#### 自動実行しない場合
「AUTO OFF」に設定
```
COPY JOB RUN {ジョブ名}
```
上のSQLをクエリスケジュールで定期実行すれば差分ロードできる



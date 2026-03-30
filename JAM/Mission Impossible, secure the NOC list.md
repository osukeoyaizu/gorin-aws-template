## task1
指示通りの名前でカスタマーマネージドキーを作成

フェデレーションユーザーをキー管理者およびキーユーザーとして追加

キーローテーションを有効化する

## task2
指示通りの名前で標準snsトピックを作成

task1で作成したカスタマーマネージドキーで暗号化

メールアドレスでサブスクリプションを作成

※確認をしないとクリアにならない

## task3
指示通りの名前でs3バケットを作成

task1で作成したカスタマーマネージドキーで暗号化(SSE-KMS)

## task4
### task3で作成したs3バケットでイベント通知の設定
※snsとkmsのポリシーを設定する必要がある

### テキストファイル作成(ファイル名:NOC_YYYYMMDD.TXT)
```
ETHAN	HUNT	TOM	CRUISE
MARISSA	WIEGLER	CATE	BLANCHETT
JASON	BOURNE	MATT	DAMON
JANE	SMITH	ANGELINA	JOLIE
```

s3バケットにファイルをアップロードする


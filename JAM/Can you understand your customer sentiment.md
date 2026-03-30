## task1
### Comprehendでジョブ作成
Name:任意

Analysis type:Sentiment

Language:English

S3 location(Input):s3://s3productreview-[region]-[account-id]/324526-product-reviews.txt

S3 location(Output):s3://s3productreview-[region]-[account-id]/output/

IAMロール:S3AccessRoleComprehend

## task2
RedshiftクラスターにIAMロール(S3AccessRoleRedshift)を関連付ける

## task3
Redshfitテーブルにs3のデータをインポートする
```
copy feedback.product_feedback
from '<ジョブで作成されたjsonファイルのs3パス>'
iam_role 'IAMARN' 
json 'auto ignorecase';
```

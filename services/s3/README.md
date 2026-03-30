## バッチオペレーション
### manifest.csv
```
{バケット名},{ファイルパス①}
{バケット名},{ファイルパス②}
{バケット名},{ファイルパス③}
```

## s3バケットをマウントする
### 前提条件
マウント先のS3バケットを作成する

空のディレクトリを作成する
### インストール
```
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install ./mount-s3.rpm -y
```

### ディレクトリをマウント
```
mount-s3 {bucket-name} {空のディレクトリ} --prefix {プレフィックス}/
```

## アクセスポイント

## Object Lambda アクセスポイント
### 前提条件
画像保存用のS3バケットとアクセスポイントを作成する

画像変換用のLambda関数を作成

LambdaのIAMロールにS3とKMSへのアクセス権を付与する

### Object Lambda アクセスポイント作成
アクセスポイント:作成したもの

S3 API:GetObject

Lambda関数:作成したもの

その他の機能:Lambda関数が範囲を使用したリクエストをサポートGetObject

### ダウンロードした画像にテキストをつけるコード
```
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, _):
    try:
        # S3 Object Lambdaのイベント情報取得
        request_route = event["getObjectContext"]["outputRoute"]
        request_token = event["getObjectContext"]["outputToken"]
        presigned_s3_url = event["getObjectContext"]["inputS3Url"]

        # 画像取得
        response = requests.get(presigned_s3_url)
        original = Image.open(io.BytesIO(response.content)).convert("RGBA")

        # ===== パラメータ設定 =====
        watermark_text = "WATERMARK"       # 文字
        font_color = (0, 0, 0, 255)        # 色 (RGBA)
        scale_factor = 10                  # サイズ倍率
        position = "center"                    # "center" または None
        custom_x = 50                      # 自分で指定するX座標
        custom_y = 100                     # 自分で指定するY座標

        # デフォルトフォント
        font = ImageFont.load_default()

        # 一時イメージ（小さめ）
        temp_img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        # テキストサイズ取得
        bbox = temp_draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 中央座標計算（temp_img内）
        tx = (temp_img.size[0] - text_width) // 2
        ty = (temp_img.size[1] - text_height) // 2

        # テキスト描画
        temp_draw.text((tx, ty), watermark_text, font=font, fill=font_color)

        # スケーリングでサイズ変更
        scaled_width = temp_img.size[0] * scale_factor
        scaled_height = temp_img.size[1] * scale_factor
        scaled_img = temp_img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

        # original画像の上に配置
        txt_layer = Image.new("RGBA", original.size, (255, 255, 255, 0))

        if position == "center":
            x = (original.size[0] - scaled_img.size[0]) // 2
            y = (original.size[1] - scaled_img.size[1]) // 2
        else:
            x, y = custom_x, custom_y  # 自分で指定

        txt_layer.paste(scaled_img, (x, y), scaled_img)

        # 合成
        output_object = Image.alpha_composite(original, txt_layer)

        # 出力
        in_mem_file = io.BytesIO()
        output_object.convert("RGB").save(in_mem_file, format="JPEG")

        # S3 Object Lambdaレスポンス
        s3.write_get_object_response(
            StatusCode=200,
            Body=in_mem_file.getvalue(),
            RequestRoute=request_route,
            RequestToken=request_token,
            ContentType="image/jpeg"
        )
        return {'status_code': 200}

    except Exception as e:
        print(f"Error: {e}")
        s3.write_get_object_response(StatusCode=500, RequestRoute=request_route, RequestToken=request_token)
        return {'status_code': 500}
```

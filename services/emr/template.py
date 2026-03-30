
import argparse
import datetime

from pyspark.sql import SparkSession


def calculate_red_violations(data_source, output_uri):
    # JST(日本時間)の現在時刻を簡易的に算出（UTC前提で+9時間）
    # ※厳密なタイムゾーン処理が必要なら zoneinfo/pytz を使う
    jst = datetime.datetime.now() + datetime.timedelta(hours=9)

    # 前日の日付(YYYY-MM-DD)を作成（パーティション名として使用）
    path_date = (jst - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 読み込み対象の前日パーティションのパスを生成
    # 例: s3://bucket/path/partition_date=2026-01-20/
    data_source = f"{data_source}/partition_date={path_date}/"

    # デバッグ出力
    print(jst)
    print(data_source)

    # Spark セッションを作成（with コンテキストで確実にクローズ）
    with SparkSession.builder.appName("Calculate Red Health Violations").getOrCreate() as spark:
        # パーティション上書き時のモードを dynamic に設定
        # （partitionBy で指定した列単位で差分上書き可能）
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

        # Parquet 読み込み（スキーママージ/推論を有効化）
        # ※ 実運用ではスキーマ推論はコストが高い場合があるため、明示スキーマ推奨
        if data_source is not None:
            df = (
                spark.read
                .option("mergeSchema", "true")
                .option("inferSchema", "true")
                .parquet(data_source)
            )

        # 一時ビューを作成して SQL で扱いやすくする
        df.createOrReplaceTempView("view")

        # デバッグ: スキーマと先頭レコードを表示
        print(">>> スキーマ:")
        df.printSchema()
        print(">>> 先頭レコード:")
        df.show(5, truncate=False)

        # 顧客・日付単位で金額を集計
        # - to_date(datetime) : タイムスタンプ/文字列列を日付に正規化
        # - SUM(amount)       : 金額の合計
        total_raw = spark.sql("""
            SELECT
              customer_id,
              to_date(datetime) AS date,
              SUM(amount)       AS total_amount
            FROM view
            GROUP BY customer_id, to_date(datetime)
        """)

        # 結果を書き出し（上書き／date でパーティション分割）
        # 例: output_uri/date=2026-01-20/ のように出力される
        total_raw.write.mode("overwrite").partitionBy("date").parquet(output_uri)


if __name__ == "__main__":
    # コマンドライン引数の定義
    parser = argparse.ArgumentParser(
        description="前日パーティションを読み込み、顧客・日付単位で amount を集計して Parquet 出力します。"
    )
    parser.add_argument(
        '--data_source',
        required=True,
        help="入力データのベースURI（例: s3://bucket/input/path）"
    )
    parser.add_argument(
        '--output_uri',
        required=True,
        help="出力先のURI（例: s3://bucket/output/path）"
    )
    args = parser.parse_args()

    # メイン処理を実行
    calculate_red_violations(args.data_source, args.output_uri)


import time
import uuid
from awscrt import mqtt
from awsiot import mqtt_connection_builder, iotshadow

# ============================================================
# 設定
# ============================================================
# AWS IoT Core のATSエンドポイント（IoT Core コンソールに表示されるもの）
ENDPOINT  = "akuwx5saizees-ats.iot.us-east-1.amazonaws.com"

# 操作対象のThing名（このThingのクラシックシャドウを扱う）
THING_B   = "ThingB"

# mTLS（相互TLS）で使う証明書ファイル
CA_FILE   = "AmazonRootCA1.pem"        # AmazonのルートCA
CERT_FILE = "ThingB.cert.pem"          # ThingB のデバイス証明書
KEY_FILE  = "ThingB.private.key"       # 証明書に対応する秘密鍵

# QoS=1: AT_LEAST_ONCE（最低1回配信）
#  - 送受信が不安定な場合でも届きやすい
#  - ただし「重複」して届く可能性があるため、同じmodeを再適用しても問題ない作りが望ましい
QOS = mqtt.QoS.AT_LEAST_ONCE


def build_connection():
    """
    AWS IoT Core へ mTLS で MQTT 接続を作成して接続する。

    ここでやっていること：
    1) 証明書/秘密鍵/CA を使って MQTT 接続オブジェクトを作る
    2) connect() で接続要求（非同期）
    3) .result() で「接続完了（CONNACK受領）」まで待ってから次へ進む
    """
    conn = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_FILE,
        pri_key_filepath=KEY_FILE,
        ca_filepath=CA_FILE,
        # client_id は MQTT 上のクライアント識別子（起動ごとに衝突しないようUUID）
        client_id=f"B-{uuid.uuid4()}",
        clean_session=True,
        keep_alive_secs=30,
    )

    # connect() は Future を返す（非同期）。result() で完了まで待つ
    conn.connect().result()
    print("[B] connected")
    return conn


def main():
    # 1) MQTT接続を確立
    mqtt_conn = build_connection()

    # 2) Shadow操作用クライアントを作成
    #    （ShadowのGET/UPDATE/DELTA購読などを簡単に扱える）
    shadow = iotshadow.IotShadowClient(mqtt_conn)

    # ============================================================
    # 共通関数：reported を更新
    # ============================================================
    def update_reported(mode: str, reason: str):
        """
        reported.mode を更新する。

        Shadowの基本：
        - desired  : クラウド側（管理側）が「こうしてほしい」状態
        - reported : デバイス側が「いまこうなっている」と報告する状態

        デバイスが desired を適用したら、その結果を reported に反映して
        desired と reported の差（delta）を解消するのが典型パターン。
        """
        # reported に {"mode": mode} を設定するリクエストを作成
        state = iotshadow.ShadowState(reported={"mode": mode})
        req = iotshadow.UpdateShadowRequest(thing_name=THING_B, state=state)

        # publish_update_shadow は「送信」するだけ（非同期）
        # accepted/rejected を購読すれば “更新が成功したか” まで追えるが、このコードではログのみ
        shadow.publish_update_shadow(req, qos=QOS)
        print(f"[B] reported updated: mode={mode} ({reason})")

    # ============================================================
    # 起動時 GET の応答（accepted / rejected）
    # ============================================================
    def on_get_accepted(resp: iotshadow.GetShadowResponse):
        """
        Shadow GET の成功応答（accepted）を受け取るコールバック。

        ここでやりたいこと：
        - 起動直後、すでに desired が設定されていても delta が “必ず” 来るとは限らない
        - そこで GET により「今の desired / reported」を取得し、
          もしズレがあれば reported を desired に追いつかせる（catch-up）
        """
        # resp.state が None のケースもあるので None-safe に扱う
        s = resp.state or {}

        # desired / reported が存在しない場合に備えて空 dict を使う
        desired = s.desired if getattr(s, "desired", None) else {}
        reported = s.reported if getattr(s, "reported", None) else {}

        # 今回は mode キーだけを見る
        d = desired.get("mode")
        r = reported.get("mode")
        print(f"[B] GET accepted: desired={d}, reported={r}")

        # desired が存在し、reported と異なるなら追いつく
        if d is not None and d != r:
            update_reported(d, reason="catch-up via GET")

    def on_get_rejected(err):
        """
        Shadow GET の失敗応答（rejected）を受け取るコールバック。

        典型例：
        - Shadow がまだ存在しない
        - 権限不足（IoTポリシー）
        - リクエスト形式が不正
        """
        print("[B] GET rejected:", err)

    # ============================================================
    # delta（desired と reported の差分通知）
    # ============================================================
    def on_delta(event: iotshadow.ShadowDeltaUpdatedEvent):
        """
        delta（差分）通知を受け取るコールバック。

        delta のポイント：
        - desired と reported に差がある “キーだけ” が event.state に入ってくる
        - ここでは state["mode"] が来たら、その mode を適用したものとして reported を更新する
        """
        delta_state = event.state or {}
        mode = delta_state.get("mode")
        print(f"[B] DELTA received: mode={mode}")

        # mode が含まれていたら追従して reported を更新
        if mode is not None:
            update_reported(mode, reason="via DELTA")

    # ============================================================
    # 1) まず購読（subscribe）を確立する
    # ============================================================
    # 重要：購読確立前に publish すると、応答が先に来て取りこぼすことがある。
    # 例えば：
    #   - GET を publish した直後に accepted が返ってきても
    #     get/accepted の購読が未確立だと受信できない
    #
    # subscribe_* は (future, topic) を返す
    #   - future : SUBSCRIBEが完了したこと（=SUBACKを受け取ったこと）を表す “完了待ちハンドル”
    #   - topic  : 実際に購読した MQTT トピック文字列（ログ/デバッグ用）
    #
    # f1,f2,f3 はこの future（購読完了を待つためのもの）。
    # .result() を呼ぶと、購読が確実に有効になるまで待てる。
    # ============================================================

    # --- GET 応答（accepted/rejected）を受け取るための購読 ---
    get_sub_req = iotshadow.GetShadowSubscriptionRequest(thing_name=THING_B)

    # f1: get/accepted の購読確立を待つ Future
    #     これが完了すると、GET成功時に on_get_accepted が呼ばれる準備が整う
    f1, topic1 = shadow.subscribe_to_get_shadow_accepted(get_sub_req, QOS, on_get_accepted)

    # f2: get/rejected の購読確立を待つ Future
    #     これが完了すると、GET失敗時に on_get_rejected が呼ばれる準備が整う
    f2, topic2 = shadow.subscribe_to_get_shadow_rejected(get_sub_req, QOS, on_get_rejected)

    # ここで必ず待つ：購読が確立してから次へ進む（取りこぼし防止）
    f1.result()
    f2.result()
    print(f"[B] subscribed GET accepted/rejected: {topic1}, {topic2}")

    # --- delta 通知を受け取るための購読 ---
    delta_req = iotshadow.ShadowDeltaUpdatedSubscriptionRequest(thing_name=THING_B)

    # f3: delta の購読確立を待つ Future
    #     これが完了すると、差分発生時に on_delta が呼ばれる準備が整う
    f3, topic3 = shadow.subscribe_to_shadow_delta_updated_events(delta_req, QOS, on_delta)

    # delta も同様に、購読確立まで待つ
    f3.result()
    print(f"[B] subscribed DELTA: {topic3}")

    # ============================================================
    # 2) 起動時 GET を 1 回送る（初回の追いつき）
    # ============================================================
    # GET は「今のShadow状態（desired / reported）を取得」するための要求。
    # 応答は get/accepted または get/rejected に返ってくる（上で購読済み）。
    shadow.publish_get_shadow(iotshadow.GetShadowRequest(thing_name=THING_B), qos=QOS)
    print("[B] published GET (initial catch-up). now waiting DELTA...")

    # ============================================================
    # 常駐（受信待ち）
    # ============================================================
    # 実際の受信処理は SDK 内部の I/O スレッドが行い、
    # メッセージ到着時に on_get_accepted / on_get_rejected / on_delta が呼ばれる。
    # ここは “プログラムを終了させないため” のループ。
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()

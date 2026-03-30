# src/inference.py
# Flask 3.x / SageMaker Hosting 対応
# - import 時にモデル＆feature_namesをロード
# - 推論時 DMatrix に学習時と同じ feature_names を必ず付与
# - 入力バリデーション・エラーハンドリング強化

from flask import Flask, request, jsonify
import os
import json
import threading
import numpy as np
import xgboost as xgb

app = Flask(__name__)

# -------------------------------
# 環境変数（SageMaker の慣習パス）
# -------------------------------
MODEL_DIR = os.environ.get("MODEL_DIR", "/opt/ml/model")
MODEL_FILE = os.environ.get("MODEL_FILE", "xgboost-model.json")
SUMMARY_FILE = os.environ.get("SUMMARY_FILE", "training_summary.json")
PORT = int(os.environ.get("PORT", "8080"))

# -------------------------------
# グローバル（スレッドセーフに扱う）
# -------------------------------
_booster = None
_feature_names = None
_init_lock = threading.Lock()


def _load_model_and_meta():
    """
    /opt/ml/model から XGBoost Booster と学習時メタ（feature_names）をロード。
    Flask 3.x / gunicorn 環境では import 時に一度実行するのが確実。
    """
    global _booster, _feature_names

    model_path = os.path.join(MODEL_DIR, MODEL_FILE)
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    b = xgb.Booster()
    b.load_model(model_path)
    _booster = b

    # feature_names は train.py が training_summary.json に保存済みを想定
    summary_path = os.path.join(MODEL_DIR, SUMMARY_FILE)
    _feature_names = None
    if os.path.isfile(summary_path):
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            feats = meta.get("features")
            if isinstance(feats, list) and all(isinstance(s, str) for s in feats):
                _feature_names = feats
        except Exception as e:
            # ログにだけ残して続行（feature_names が無い場合は validate_features=False で回避可）
            print(f"[Warn] Failed to read summary ({summary_path}): {e}", flush=True)

    print(f"[Init] Loaded model: {model_path}", flush=True)
    print(f"[Init] feature_names: {_feature_names}", flush=True)


def _ensure_loaded():
    """多重起動時でも一度だけロードされるように保険をかける。"""
    global _booster
    if _booster is None:
        with _init_lock:
            if _booster is None:
                _load_model_and_meta()


# import 時にロード（SageMaker の gunicorn がモジュール import 時に実行）
try:
    _load_model_and_meta()
except Exception as e:
    # 起動直後に失敗しても、後続の _ensure_loaded() で再挑戦できるようにログだけ出す
    print(f"[Warn] Initial model load failed: {e}", flush=True)


@app.route("/ping", methods=["GET"])
def ping():
    """
    モデルがロードできているかを返す。
    - 200: 正常
    - 500: モデル未ロード
    """
    return ("", 200) if _booster is not None else ("", 500)


@app.route("/invocations", methods=["POST"])
def invocations():
    """
    入力: application/json
      {"instances": [[f0,f1,...,fN], [f0,f1,...], ...]}
    出力:
      {"predictions":[y1, y2, ...]}
    ※ 特徴量の順序・スケールは学習時と同一に揃えてください。
    """
    try:
        _ensure_loaded()

        payload = request.get_json(force=True, silent=False)
        if not isinstance(payload, dict) or "instances" not in payload:
            return jsonify({"error": "Request body must be JSON with key 'instances'"}), 400

        instances = payload["instances"]
        if not isinstance(instances, list) or len(instances) == 0:
            return jsonify({"error": "instances must be a non-empty list"}), 400

        # 数値配列へ（ここで文字列や None が混じっていると ValueError）
        X = np.array(instances, dtype=float)  # shape: (batch, n_features)
        if X.ndim != 2:
            return jsonify({"error": "instances must be a 2D list: [[...],[...],...]"}), 400

        # 学習時の feature_names がある場合は必ず合わせる
        # ない場合は validate_features=False で整合チェックを緩和（本番では揃えるのが望ましい）
        if _feature_names is not None:
            # 列数チェック（ズレていれば明示的にエラー）
            if X.shape[1] != len(_feature_names):
                return jsonify({
                    "error": "feature dimension mismatch",
                    "detail": {
                        "received_n_features": int(X.shape[1]),
                        "expected_n_features": int(len(_feature_names)),
                        "expected_feature_names": _feature_names
                    }
                }), 400

            dmat = xgb.DMatrix(X, feature_names=_feature_names)
            preds = _booster.predict(dmat).tolist()
        else:
            # 応急処置：学習時に feature_names を付けていない前提でチェックを無効化
            dmat = xgb.DMatrix(X)
            preds = _booster.predict(dmat, validate_features=False).tolist()

        return jsonify({"predictions": preds})

    except ValueError as ve:
        # 代表例: feature_names mismatch / 変換できない値が混入
        return jsonify({"error": "invalid input", "detail": str(ve)}), 400
    except FileNotFoundError as fe:
        return jsonify({"error": "model_not_found", "detail": str(fe)}), 500
    except xgb.core.XGBoostError as xe:
        return jsonify({"error": "xgboost_error", "detail": str(xe)}), 500
    except Exception as e:
        # 予期しない例外は 500
        return jsonify({"error": "internal_error", "detail": str(e)}), 500


if __name__ == "__main__":
    # ローカルデバッグ用（SageMaker 本番では gunicorn が使われる）
    app.run(host="0.0.0.0", port=PORT, debug=False)

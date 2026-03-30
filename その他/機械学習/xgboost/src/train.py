import os
import argparse
import json
import pandas as pd
import xgboost as xgb


def parse_args():
    parser = argparse.ArgumentParser()

    # データと出力のパス（SageMaker のお約束パス）
    parser.add_argument("--train_channel", default="/opt/ml/input/data/train")
    parser.add_argument("--validation_channel", default="/opt/ml/input/data/validation")
    parser.add_argument("--model_dir", default="/opt/ml/model")
    parser.add_argument("--output_dir", default="/opt/ml/output/intermediate")

    # XGBoost のハイパーパラメータ
    parser.add_argument("--objective", default="reg:squarederror")
    parser.add_argument("--eval_metric", default="rmse")
    parser.add_argument("--num_boost_round", type=int, default=200)
    parser.add_argument("--max_depth", type=int, default=5)
    parser.add_argument("--eta", type=float, default=0.2)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--colsample_bytree", type=float, default=0.8)
    parser.add_argument("--reg_lambda", type=float, default=1.0)
    parser.add_argument("--reg_alpha", type=float, default=0.0)
    parser.add_argument("--early_stopping_rounds", type=int, default=30)

    # SageMaker が余計な引数を渡してきても無視できるようにする
    args, _ = parser.parse_known_args()
    return args


def read_first_csv_noheader(dir_path: str) -> pd.DataFrame:
    """指定ディレクトリ内の最初の CSV をヘッダーなしで読む（先頭列が目的変数）"""
    files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]
    if not files:
        raise RuntimeError(f"No CSV found in {dir_path}")
    csv_path = os.path.join(dir_path, files[0])
    return pd.read_csv(csv_path, header=None)


def to_dmatrix(df: pd.DataFrame):
    """先頭列を y、それ以外を X として DMatrix を作る"""
    y = df.iloc[:, 0].to_numpy()
    X = df.iloc[:, 1:].to_numpy()
    feature_names = [f"f{i}" for i in range(X.shape[1])]
    dmatrix = xgb.DMatrix(X, label=y, feature_names=feature_names)
    return dmatrix, feature_names


def main():
    args = parse_args()

    os.makedirs(args.model_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    # --- train データ ---
    train_df = read_first_csv_noheader(args.train_channel)
    dtrain, feature_names = to_dmatrix(train_df)

    # --- validation データ（あれば）---
    evals = [ (dtrain, "train") ]
    dvalid = None

    if os.path.isdir(args.validation_channel):
        has_csv = any(f.endswith(".csv") for f in os.listdir(args.validation_channel))
        if has_csv:
            valid_df = read_first_csv_noheader(args.validation_channel)
            dvalid, _ = to_dmatrix(valid_df)
            evals.append((dvalid, "validation"))

    # --- XGBoost のパラメータ ---
    params = {
        "objective": args.objective,
        "eval_metric": args.eval_metric,
        "eta": args.eta,
        "max_depth": args.max_depth,
        "subsample": args.subsample,
        "colsample_bytree": args.colsample_bytree,
        "lambda": args.reg_lambda,
        "alpha": args.reg_alpha,
        "verbosity": 1,
    }

    # --- 学習 ---
    bst = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=args.num_boost_round,
        evals=evals,
        early_stopping_rounds=(args.early_stopping_rounds if dvalid is not None else None),
    )

    # --- モデル保存（SageMaker が /opt/ml/model を S3 にアップロード）---
    model_path = os.path.join(args.model_dir, "xgboost-model.json")
    bst.save_model(model_path)

    # --- 学習情報も保存 ---
    summary_path = os.path.join(args.output_dir, "training_summary.json")
    with open(summary_path, "w") as f:
        json.dump(
            {
                "features": feature_names,
                "best_iteration": getattr(bst, "best_iteration", None),
            },
            f,
        )

    print(f"Saved model to: {model_path}")
    print(f"Saved training summary to: {summary_path}")


if __name__ == "__main__":
    main()


# pipeline.py
import os
from datetime import datetime

import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.function_step import step
from sagemaker.workflow.parameters import ParameterString, ParameterInteger

# 条件分岐
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.conditions import ConditionEquals

# Lambda をパイプラインから呼ぶ
from sagemaker.workflow.lambda_step import (
    LambdaStep,
    LambdaOutput,
    LambdaOutputTypeEnum,
)
from sagemaker.lambda_helper import Lambda as SmLambda

# CallbackStep（外部からのコールで再開させる待機ステップ）
from sagemaker.workflow.callback_step import (
    CallbackStep,
    CallbackOutput,
    CallbackOutputTypeEnum,
)

# あなたの関数（Function Step 化）
from preprocess import preprocess
from train import train
from evaluation import evaluate
from register import register


def _get_role_arn(sm_session: sagemaker.session.Session) -> str:
    """
    実行ロールを解決します。
    1) Studio/ノートブックからの実行: get_execution_role()
    2) 環境変数 SAGEMAKER_ROLE_ARN
    3) セッションから Caller Identity
    """
    try:
        return sagemaker.get_execution_role()
    except Exception:
        env_role = os.getenv("SAGEMAKER_ROLE_ARN")
        if env_role:
            return env_role
        return sm_session.get_caller_identity_arn()


if __name__ == "__main__":
    # Remote Function の設定ファイル（config.yaml）をこのフォルダで上書き
    os.environ["SAGEMAKER_USER_CONFIG_OVERRIDE"] = os.getcwd()

    sm_session = sagemaker.session.Session()
    region = sm_session.boto_region_name
    role_arn = _get_role_arn(sm_session)

    # ========= 実行時パラメータ =========
    input_path = ParameterString(
        name="InputDataS3Uri",
        default_value=(
            f"s3://sagemaker-example-files-prod-{region}/datasets/"
            f"tabular/uci_abalone/abalone.csv"
        ),
    )
    model_pkg_group_name = ParameterString(
        name="ModelPackageGroupName",
        default_value="abalone-model-new-sdk",
    )

    # デプロイ関連（必要に応じて上書き）
    endpoint_name_param = ParameterString(
        name="EndpointName",
        default_value="abalone-endpoint",
    )
    endpoint_config_name_param = ParameterString(
        name="EndpointConfigName",
        default_value="abalone-endpoint-config",
    )
    endpoint_instance_type_param = ParameterString(
        name="EndpointInstanceType",
        default_value="ml.m5.xlarge",
    )
    endpoint_initial_instance_count_param = ParameterInteger(
        name="EndpointInitialInstanceCount",
        default_value=1,
    )

    # ========= 外部サービス（環境変数で指定） =========
    # ※ 実行リージョン（region）と一致するリソースを使ってください
    approval_sqs_url = os.getenv(
        "APPROVAL_SQS_URL",
        "https://sqs.us-east-1.amazonaws.com/140083316867/approval-sqs",
    )

    status_checker_lambda_arn = os.getenv(
        "STATUS_CHECK_LAMBDA_ARN",
        "arn:aws:lambda:us-east-1:140083316867:function:status_check",
    )
    status_checker_lambda = SmLambda(
        function_arn=status_checker_lambda_arn,
        session=sm_session,
    )

    deployer_lambda_arn = os.getenv(
        "DEPLOYER_LAMBDA_ARN",
        "arn:aws:lambda:us-east-1:140083316867:function:step-lambda",
    )
    deployer_lambda = SmLambda(
        function_arn=deployer_lambda_arn,
        session=sm_session,
    )

    # ========= 共通情報 =========
    bucket = sm_session.default_bucket()

    # 実行ごとの一意なプレフィックス（学習成果物の格納先）
    run_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    s3_output_prefix = f"s3://{bucket}/abalone/models/{run_id}"

    # ========= Function Steps =========
    data = step(
        preprocess,
        name="Abalone_Data_Preprocessing",
        instance_type="ml.m5.xlarge",
    )(input_path)

    # train() は「学習済みモデルの S3 URI（model.tar.gz）」を返す実装にしてください
    model = step(
        train,
        name="Model_Training",
        instance_type="ml.m5.xlarge",
    )(
        train_df=data[0],
        validation_df=data[1],
        s3_output_prefix=s3_output_prefix,   # ← 学習成果物の格納先（実行ごとに一意）
    )

    evaluation_result = step(
        evaluate,
        name="Model_Evaluation",
        instance_type="ml.m5.xlarge",
    )(
        model_data_s3_uri=model,  # ← train() が返す S3 URI
        test_df=data[2],
    )

    # Register は PendingManualApproval で固定（後から手動承認）
    model_register = step(
        register,
        name="Model_Registration",
        instance_type="ml.m5.xlarge",
    )(
        model_data_s3_uri=model,          # ← train ステップが返す S3 URI
        evaluation=evaluation_result,
        model_approval_status="PendingManualApproval",
        model_package_group_name=model_pkg_group_name,
        bucket=bucket,
        role_arn=role_arn,
    )
    # ↑ Pipeline 変数として ModelPackageArn（文字列）が入る想定

    # ========= 承認待ち：CallbackStep =========
    # Register 完了後にメッセージを送るよう依存関係を明示（ModelPackageArn が arguments に入る）
    wait_for_approval = CallbackStep(
        name="Wait_For_Manual_Approval",
        sqs_queue_url=approval_sqs_url,
        inputs={"ModelPackageArn": model_register},
        outputs=[CallbackOutput(output_name="Ack", output_type=CallbackOutputTypeEnum.String)],
        depends_on=[model_register],  # ★ 重要：これで arguments に ModelPackageArn が入る
    )

    # ========= 実際の ModelPackage 承認状態を Describe する LambdaStep =========
    status_step = LambdaStep(
        name="Get_ModelPackage_Approval_Status",
        lambda_func=status_checker_lambda,
        inputs={"ModelPackageArn": model_register},
        outputs=[
            LambdaOutput(output_name="ApprovalStatus", output_type=LambdaOutputTypeEnum.String),
        ],
        depends_on=[wait_for_approval],  # Callback 再開後に実行
    )

    # ========= デプロイ（Lambda 経由） =========
    lambda_inputs = {
        "ModelPackageArn": model_register,              # 登録したモデルパッケージ ARN（Pipeline 変数OK）
        "RoleArn": role_arn,
        "ModelName": f"abalone-model-from-pkg-{run_id}",  # 一意な名前にして競合回避
        "EndpointConfigName": endpoint_config_name_param,
        "EndpointName": endpoint_name_param,
        "InstanceType": endpoint_instance_type_param,
        "InitialInstanceCount": endpoint_initial_instance_count_param,
    }
    lambda_outputs = [
        LambdaOutput(output_name="EndpointName", output_type=LambdaOutputTypeEnum.String),
    ]

    deploy_step = LambdaStep(
        name="Deploy_Endpoint_Via_Lambda",
        lambda_func=deployer_lambda,
        inputs=lambda_inputs,
        outputs=lambda_outputs,
    )

    # ========= 条件：Describe の結果が Approved のときだけデプロイ =========
    deploy_if_approved = ConditionStep(
        name="Deploy_If_Approved",
        conditions=[
            ConditionEquals(
                left=status_step.properties.Outputs["ApprovalStatus"],   # ← 実際の承認状態
                right="Approved",
            )
        ],
        if_steps=[deploy_step],
        else_steps=[],
    )

    # ========= パイプライン定義 =========
    pipeline = Pipeline(
        name="abalone-sm-pipeline-approved-on-event",
        parameters=[
            input_path,
            model_pkg_group_name,
            endpoint_name_param,
            endpoint_config_name_param,
            endpoint_instance_type_param,
            endpoint_initial_instance_count_param,
        ],
        steps=[
            data,
            model,
            evaluation_result,
            model_register,
            wait_for_approval,      # ここで一旦停止（承認イベントを待つ）
            status_step,            # 再開後に承認状態を確認
            deploy_if_approved,     # Approved ならデプロイ
        ],
    )

    # ========= 作成＆実行 =========
    pipeline.upsert(role_arn=role_arn)
    # 実行開始（CallbackStep で待機に入る。Approved で EventBridge→Lambda が再開させる）
    start_resp = pipeline.start()
    print(f"Pipeline execution started: {start_resp.arn}")

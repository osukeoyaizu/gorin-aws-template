## AWS CodePipeline 変数一覧表（Markdown版）

### 1. グローバル変数
- `#{codepipeline.PipelineExecutionId}`: パイプライン実行 ID。

### 2. パイプラインレベル変数
- `#{variables.MY_PARAM}`: v2 パイプライン実行時入力。

### 3. アクション出力変数
#### CodeCommit
- `#{SourceVariables.CommitId}`: コミット ID。
- `#{SourceVariables.BranchName}`: ブランチ名。
- `#{SourceVariables.RepositoryName}`: リポジトリ名。
- `#{SourceVariables.CommitMessage}`: コミットメッセージ。

#### S3
- `#{SourceVariables.BucketName}`: S3 バケット名。
- `#{SourceVariables.ObjectKey}`: オブジェクトキー。
- `#{SourceVariables.ETag}`: ETag。
- `#{SourceVariables.VersionId}`: バージョン ID。

#### CodeStar/GitHub
- `#{SourceVariables.CommitId}`: コミット SHA。
- `#{SourceVariables.BranchName}`: ブランチ名。
- `#{SourceVariables.FullRepositoryName}`: 完全リポジトリ名。
- `#{SourceVariables.CommitMessage}`: コミットメッセージ。

#### ECR
- `#{SourceVariables.RegistryId}`: レジストリ ID。
- `#{SourceVariables.RepositoryName}`: リポジトリ名。
- `#{SourceVariables.ImageTag}`: イメージタグ。
- `#{SourceVariables.ImageDigest}`: イメージダイジェスト。
- `#{SourceVariables.ImageURI}`: イメージ URI。

#### CodeBuild
- `#{BuildVariables.<YourVariable>}`: buildspec の exported-variables で公開した値。

#### CloudFormation
- `#{UpstreamCf.Outputs.MyValue}`: 上流 CFN 出力値。

#### Lambda
- `#{LambdaVariables.MyOutput}`: Lambda アクション出力。

### 注意点
- 変数は CodePipeline のアクション設定で定義する必要がある。
- 名前空間を設定しないと参照できない。
- CodeDeploy では直接参照不可。

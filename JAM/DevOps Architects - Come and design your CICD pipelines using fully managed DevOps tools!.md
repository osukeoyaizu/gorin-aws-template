## task1
CodeArtifactのリポジトリ(abc-codeartifact-repo)を編集し、アップストリームリポジトリで、「upstream-to-pypi-store」を関連付ける

## task2
CodeArtifactのリポジトリ(abc-codeartifact-repo)のリポジトリポリシーを以下に変更
```
"codeartifact:DescribePackageVersion",
"codeartifact:DescribeRepository",
"codeartifact:GetPackageVersionReadme",
"codeartifact:GetRepositoryEndpoint",
"codeartifact:ListPackageVersionAssets",
"codeartifact:ListPackageVersionDependencies",
"codeartifact:ListPackageVersions",
"codeartifact:ListPackages",
"codeartifact:PublishPackageVersion",
"codeartifact:PutPackageMetadata",
"codeartifact:ReadFromRepository"
```

CodePipeline(abc-helloworld-codepipeline)の変更をリリースする

abc-helloworld-codepipelineが成功後にabc-app-codepipelineの変更をリリースして成功させる

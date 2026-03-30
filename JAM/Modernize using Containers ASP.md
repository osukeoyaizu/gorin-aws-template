## task1
### Source-NET-Webserverのセキュリティグループのインバウンドルール追加
タイプ:WinRM-HTTPS

ソース:インスタンス(App2C-Server)のセキュリティグループ

```
app2container init
```
※s3バケットを入力する

```
app2container remote configure
```
※NETWebAppIPAddressとシークレットARNを入力する

## task2
```
app2container remote inventory --target <NETWebAppIPAddress>
```
※C:\Users\Administrator\AppData\Local\app2container\remote\[NETWebAppIPAddress]\inventory.json内からアプリケーションIDをコピーする
```
app2container remote analyze --target <NETWebAppIPAddress> --application-id <application-id>
```

C:\Users\Administrator\AppData\Local\app2container\remote\[NETWebAppIPAddress]\[application-id]\analysis.jsonからsitePhysicalPathをコピーする
```
C:\\Unicornshop
```

## task3
```
app2container remote extract --target <NETWebAppIPAddress> --application-id <application-id>
```

※Next Step:で表示されたコマンドを実行すればいい
```
app2container containerize --input-archive C:\Users\Administrator\AppData\Local\app2container\remote\[NETWebAppIPAddress]\[application-id]\[application-id].zip
```

※C:\Users\Administrator\AppData\Local\app2container\[application-id]\Artifacts 配下のDockerFileのFROMの値を回答する
```
mcr.microsoft.com/dotnet/framework/aspnet:4.8-windowsservercore-ltsc2019
```

## task4
```
app2container generate app-deployment --application-id [application-id]
```

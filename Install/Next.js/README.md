## install手順(amazonlinux2023)
```
sudo yum install -y npm 
sudo npm install -y npx 
```

## アプリ作成・起動
```
npx create-next-app -e hello-world appname
cd appname
npm run build
npm start
```

※ポートを指定する場合
PORT=4000 npm start

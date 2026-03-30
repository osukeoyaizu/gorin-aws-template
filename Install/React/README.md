## install手順(amazonlinux2023)
https://qiita.com/sueasen/items/c5ac3e99b021d04a5cc0
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
node -e "console.log('Running Node.js ' + process.version)"
```

## アプリ作成
```
npx create-react-app <プロジェクト名>
```

## アプリ起動
```
cd <プロジェクト名>
npm start
```

※ポートを指定する場合
PORT=4000 npm start

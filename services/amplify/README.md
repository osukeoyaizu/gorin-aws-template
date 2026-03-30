## Amplify CLI
### インストール
```
npm install -g @aws-amplify/cli
amplify --version
```

### Reactアプリ作成
```
npx create-react-app app
cd app
```

### Amplify プロジェクトを初期化
```
amplify init
```

### 認証機能追加

#### 認証（Auth = Cognito）追加
```
amplify add auth
```

#### クラウドへ反映
```
amplify push
```

#### 依存ライブラリ追加
```
npm i aws-amplify @aws-amplify/ui-react
```

#### src/index.jsを編集
```
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

import reportWebVitals from './reportWebVitals';
import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';

Amplify.configure(awsExports);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

```


#### App.jsを編集
```
import { withAuthenticator } from '@aws-amplify/ui-react';

function App() {
  return <h1>ログイン完了！この画面は認証済みユーザーだけが見られます。</h1>;
}

export default withAuthenticator(App);
```


#### ホスティング追加
**※AmplifyでもS3+CloudFrontでも可能**
```
amplify add hosting
```

#### ビルド & 公開
```
npm run build
amplify publish
```

const API_BASE_URL = 'http://example.com/api';
const COGNITO_USER_POOL_DOMAIN = 'us-east-1xxxxxxxxx';
const COGNITO_CLIENT_ID = 'xxxxxxxxxx';
const CALLBACK_URL = 'http://example.com';

// CognitoのホストされたUIのURL
const cognitoLoginUrl = `https://${COGNITO_USER_POOL_DOMAIN}.auth.ap-northeast-1.amazoncognito.com/login?client_id=${COGNITO_CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri=${CALLBACK_URL}`;

// サインインボタンのクリックイベント
document.getElementById('signinButton').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = cognitoLoginUrl; // Cognitoのログインページにリダイレクト
});

// Cognitoを使用した認証処理
async function getToken() {
    let token = localStorage.getItem('token');
    const params = new URLSearchParams(window.location.search);
    const authCode = params.get('code');
    
    if (!token && authCode) {
        const requestBody = new URLSearchParams();
        requestBody.append('grant_type', 'authorization_code');
        requestBody.append('client_id', COGNITO_CLIENT_ID);
        requestBody.append('code', authCode);
        requestBody.append('redirect_uri', CALLBACK_URL);
    
        await fetch(`https://${COGNITO_USER_POOL_DOMAIN}.auth.ap-northeast-1.amazoncognito.com/oauth2/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: requestBody.toString(),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('トークン取得に失敗しました');
            }
            return response.json();
        })
        .then(data => {
            token = data.id_token;
            localStorage.setItem('token', token);
        })
        .catch(error => {
            console.error('エラー:', error);
            alert('トークン取得中にエラーが発生しました: ' + error.message);
        });
    } else {
        console.log('認証コードが見つかりません');
    }
    return token;
}

// Authorizationヘッダーを取得
async function getAuthorizationHeader() {
    const token = await getToken();
    return token ? `Bearer ${token}` : ''; // Bearerトークン形式で返す
};

// APIからデータ取得
async function fetchData() {
    try {
        const response = await fetch(`${API_BASE_URL}`, {
            headers: {
                'Authorization': await getAuthorizationHeader()
            }
        });
        if (!response.ok) {
            throw new Error('データ取得に失敗しました');
        }
        const data = await response.json();

        // テーブルをクリア
        dataTableBody.innerHTML = '';

        // データをテーブルに挿入
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><a href="/emotion.html?id=${item.id}">${item.id}</a></td>
                <td>${item.name}</td>
            `;
            dataTableBody.appendChild(row);
        });
    } catch (error) {
        alert('エラーが発生しました: ' + error.message);
        console.error('エラー:', error);
    }
}

// 初回データ取得
document.addEventListener('DOMContentLoaded', async () => {
    await fetchData();
});
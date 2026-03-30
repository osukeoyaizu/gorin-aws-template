const API_BASE_URL = 'https://xxxxx/api';

// データ更新
const postButton = document.getElementById('postButton');
postButton.addEventListener('click', async () => {
    const inputText = document.getElementById('textInput').value;
    await fetch(`${API_BASE_URL}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Failed to post.');
            });
        }
        alert('Posted successfully.');
    })
    .catch(error => {
        console.error('Error sending data:', error);
        alert('Failed to post.');
    });
});
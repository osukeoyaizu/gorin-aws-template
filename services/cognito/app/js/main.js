// JSONデータを取得するURL
const url = "https://mnt9hvynl6.execute-api.ap-northeast-1.amazonaws.com/dev";

// テーブルを生成する関数
function createTable(data) {
  // テーブル要素を作成
  var table = document.createElement("table");

  // テーブルヘッダーを作成
  var thead = document.createElement("thead");
  var headerRow = document.createElement("tr");
  for (var key in data[0]) {
    var th = document.createElement("th");
    th.textContent = key;
    headerRow.appendChild(th);
  }
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // テーブルボディを作成
  var tbody = document.createElement("tbody");
  data.forEach(function(obj) {
    var row = document.createElement("tr");
    for (var key in obj) {
      var cell = document.createElement("td");
      cell.textContent = obj[key];
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  });
  table.appendChild(tbody);

  // テーブルをbody要素に追加
  document.body.appendChild(table);
}

// JSONデータを取得する関数
function fetchJSONData(url) {
  // トークンを取得
  var token = sessionStorage.getItem("accessToken");
  if (!token) {
    alert("認証を行ってください");
    window.location.href = "/auth.html";
  }
  fetch(url, {
      headers: {
        Authorization: "Bearer " + token
      }
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(function(data) {
      createTable(data);
    })
    .catch(function(error) {
      console.log("Error: " + error.message);
    });
}

// JSONデータを取得してテーブルを生成
var table = fetchJSONData(url);

var dataElement = document.getElementById("data");
dataElement.innerHTML = table;
## task1
何もしなくてもクリア

## task2
### BedrockのChat / Text playgroundを使用
モデル: Nova Lite と Nova Micro
### プロンプト
```
Generate a story for a new game character. The character is a gatekeeper to a mystical world. The gatekeeper is approached by a traveler looking for an entrance to the mystical world. The gatekeeper must present the traveler with three options:
```

## task3
### BedrockのChat / Text playgroundを使用

**※プロンプトはtask2と同じ**

#### 1回目
モデル: Nova Lite

temperature = 0.9

Top P = 0.9

Length = 1000


#### 2回目
モデル: Nova Lite

temperature = 0.1

Top P = 0.1

Length = 1024


## task4
### BedrockのImage generation playgroundを使用
モデル: Nova Canvas

Prompt strength:10

**※プロンプトはtask2と同じ**


## task5
```
{"max_new_tokens": 2048, "temperature" : 0.6, "top_p":0.7}
```

## task1
### エージェントのアクショングループのインラインオープンAPIスキーマを編集する
```
openapi: 3.0.0
info:
  title: Home Security System API
  version: 1.0.0
  description: API for analyzing rooms in a house to detect intruders using image processing
paths:
  /security:
    post:
      summary: Analyze a room for intruders
      description: Analyze images from a specific room to detect if there are any intruders present
      operationId: analyzeRoom
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                room:
                  type: string
                  description: The room to analyze (bedroom1, bedroom2, frontdoor, hall, garden, kitchen)
                teacher:
                  type: string
                  description: The room to analyze (bedroom1, bedroom2, frontdoor, hall, garden, kitchen)
                query:
                  type: string
                  description: User's security query
              required:
              - room
      responses:
        "200":
          description: Successful analysis
          content:
            application/json:
              schema:
                type: object
                properties:
                  room:
                    type: string
                    description: The room that was analyzed
                  status:
                    type: string
                    description: Status of the room (INTRUDER DETECTED or Secure)
                  summary:
                    type: string
                    description: Summary of whether an intruder is found and in which room
                  timestamp:
                    type: string
                    description: Timestamp of the analysis
                  detection_result:
                    type: object
                    description: Results from person detection
                    properties:
                      persons_detected:
                        type: integer
                        description: Number of persons detected in the room
                      has_intruder:
                        type: boolean
                        description: Whether an intruder was detected
                  confidence:
                    type: number
                    description: Confidence score of the detection (0-100)
                  rekognition_confidence:
                    type: number
                    description: Confidence score of the detection with rekognition (0-100)
                  bedrock_confidence:
                    type: number
                    description: Confidence score of the detection with bedrock (0-100)
                  analysis:
                    type: string
                    description: Detailed analysis from Bedrock model
                  objects_detected:
                    type: array
                    description: All objects detected in the room
                    items:
                      type: string
                  room_details:
                    type: object
                    description: Details about the room being analyzed
                    properties:
                      name:
                        type: string
                        description: Name of the room
                      objects:
                        type: array
                        description: Objects detected in the room
                        items:
                          type: string
                  intruder_location:
                    type: string
                    description: The room where the intruder is found
        "400":
          description: Bad request - Invalid input parameters
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    description: Error message
                  error:
                    type: string
                    description: Detailed error information
        "403":
          description: Access denied - Security guardrail triggered
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    description: Access denied message
                  reason:
                    type: string
                    description: Reason for access denial
        "404":
          description: Image not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    description: Error message
                  error:
                    type: string
                    description: Detailed error information
                  room:
                    type: string
                    description: The room that was requested
        "500":
          description: Server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    description: Error message
                  error_type:
                    type: string
                    description: Type of error
                  error_details:
                    type: string
                    description: Detailed error information
                  timestamp:
                    type: string
                    description: Timestamp of the error
```

保存して終了、準備をクリック

エイリアスを編集し、新しいバージョンを作成し、このエイリアスに関連付けますを選択する


### アプリケーションを実行する
コマンドプロンプトで出力プロパティのApplicationCredentialsを実行し、認証情報を取得する

アプリケーションにログインし、「Bedrock Agent ID」、「Bedrock Agent Alias ID」の値を入力する

「Where is the intruder in the house?」と質問する


## task2
エージェントにガードレールを紐づける

エイリアスを編集し、新しいバージョンを作成し、このエイリアスに関連付けますを選択する


## task3
Lambda関数(aws-jam-challenge-lambda)の環境変数を編集

CONFIDENCE_THRESHOLD:95.0

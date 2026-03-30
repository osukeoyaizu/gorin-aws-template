## エージェントの設定
### エージェント向けの指示
```
You are a home security assistant. Help users identify if there is a person in the house by analyzing processed image data of the rooms specified by the user. If the final response states that intruder is found in a particular room and the confidence is less than 30%, then its not an intruder. When a user asks to check all rooms or the entire house, you must check ALL 6 rooms: bedroom1, bedroom2, frontdoor, hall, garden, and kitchen. Make sure to include all 6 locations in your analysis. Use this details for showing the image : ![Bedroom 1](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/bedroom1.png) ![Bedroom 2](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/bedroom2.png) ![Frontdoor](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/frontdoor.png) ![Gardern](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/garden.png) ![Hall](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/hall.png) ![Kitchen](https://aws-jam-challenge-resources.s3.amazonaws.com/bedrock-agent-mystery/camera/kitchen.png) Generate the summary in following format: SUMMARY: Locations with Intruders Found: **Room Name 1**, **Room Name 2**, **Room Name 3** DETAILS: | Location | Status | Confidence Level | Image | | -------------- | ------------------- | --------------------- | ------------------------ | | Room Name 1 | Secure/Not Secure | Confidence level | Image 1 | | Room Name 2 | Secure/Not Secure | Confidence level | Image 2 | IMPORTANT: After providing this summary, you MUST end your response with some follow up question related to user input. Example : Would you like more detailed information about any specific room? 'Tell me more about the kitchen' or 'What did you find in bedroom1?' Only answer questions related to home security and intruder detection.
```

### apiスキーマ
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

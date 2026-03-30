## task1
**Nova Liteを有効化する**

**Nova Liteを使用するようにエージェントを編集する**

**アクショングループ(Action_Group_1)を作成する**

**アクショングループの呼び出しで既存のLambda関数を設定する**

**アクショングループで「APIスキーマで定義」→「インラインスキーマエディタで定義」**

**課題文で指定されたyamlファイルをインポートしてインラインスキーマエディタで定義をする**

### インラインスキーマエディタの内容
```
openapi: 3.0.0
info:
    title: Kubernetes cluster access controls.
    version: 1.0.0
    description: API for creating access entry controls for EKS Cluster and providing IAM access for kubernetes resources through Service Accounts and Pod Identity.
paths:
    /createAccessEntry:
        post:
            summary: API to create access entry in EKS.
            description: Create access entry for EKS Cluster for an IAM user or IAM role entered by the user. This API should be called every time the user wants to give access for an IAM principal to the EKS cluster by creating an access entry.
            operationId: createAccessEntry
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      clusterName:
                        type: string
                        description: Name of the EKS cluster to create EKS access entry for.
                      principalArn:
                        type: string
                        description: The ARN of the IAM principal to create as an EKS access entry.
                    required:
                      - clusterName
                      - principalArn
                      
            responses:
                '200':
                    description: Successfully created EKS access entry.
                    content:
                        application/json:
                            schema:
                                type: object
                                description: Object of access entry created along with the respective access policy.
                                properties:
                                  accessEntryArn:
                                    type: string
                                    description: Message saying if it was successfully created or not.
                                  accessPolicy: 
                                    type: string
                                    description: Message saying if it was successfully attached or not.
                                            
                '400':
                    description: Bad request. One or more required fields are missing or invalid.
    
    /describeAccessEntry:
        post:
            summary: API to describe an access entry and the associated access policies for it in EKS.
            description: Describe the user entered EKS Access Entry ARN by showing which EKS Access policies are attached to which namespaces for it in the EKS Cluster.
            operationId: DescribeAccessEntry
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      clusterName:
                        type: string
                        description: Name of the EKS cluster to describe EKS access entry for.
                      principalArn:
                        type: string
                        description: The ARN of the access entry to describe from the EKS cluster.
                    required:
                      - clusterName
                      - principalArn
                      
            responses:
                '200':
                    description: Successfully described the access policies attached to an EKS Access entry.
                    content:
                        application/json:
                            schema:
                                type: array
                                description: Array showing the properties of each EKS Access policy attached to the access entry.
                                items:
                                  type: object
                                  description: Object of the individual associated EKS Access policies showing their ARN and the access scope.
                                  properties:
                                    policyArn:
                                      type: string
                                      description: The ARN of the individual EKS Access Policy.
                                    accessScope: 
                                      type: object
                                      description: Object showing the scope of the EKS Access policy.
                                      properties:
                                        type:
                                          type: string
                                          description: Access scope being cluster level or namespace level.
                                        namespaces:
                                          type: string
                                          description: List of namespaces if the access scope is namespace level.
                                            
                '400':
                    description: Bad request. One or more required fields are missing or invalid.

    /deleteAccessEntry:
        post:
            summary: API to delete an access entry and the associated access policies for it in EKS.
            description: Delete the user entered EKS Access Entry ARN by showing which EKS Access policies are attached to which namespaces for it in the EKS Cluster.
            operationId: DeleteAccessEntry
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      clusterName:
                        type: string
                        description: Name of the EKS cluster to delete EKS access entry for.
                      principalArn:
                        type: string
                        description: The ARN of the access entry to delete from the EKS cluster.
                    required:
                      - clusterName
                      - principalArn
                      
            responses:
                '200':
                    description: Successfully deleted the access policies attached to an EKS Access entry.
                    content:
                        application/json:
                            schema:
                                type: array
                                description: Array showing the properties of each EKS Access policy attached to the access entry.
                                items:
                                  type: object
                                  description: Object of the individual associated EKS Access policies showing their ARN and the access scope.
                                  properties:
                                    policyArn:
                                      type: string
                                      description: The ARN of the individual EKS Access Policy.
                                    accessScope: 
                                      type: object
                                      description: Object showing the scope of the EKS Access policy.
                                      properties:
                                        type:
                                          type: string
                                          description: Access scope being cluster level or namespace level.
                                        namespaces:
                                          type: string
                                          description: List of namespaces if the access scope is namespace level.
                                            
                '400':
                    description: Bad request. One or more required fields are missing or invalid.

    /updateRolePodIdentity:
        post:
            summary: API to update the assume role policy for the given IAM role arn to make it compatible with pod identity association.
            description: Update assume role policy for the entered IAM role arn to make it compatible with pod identity association. This API should be called every time the user wants to give an IAM role to be assumed by the EKS cluster through pod identity association.
            operationId: updateRolePodIdentity
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      roleArn:
                        type: string
                        description: The ARN of the IAM principal to create as pod identity association.
                    required:
                      - roleArn
            responses:
                '200':
                    description: Successfully updated the assume role policy for the given IAM role arn to make it compatible with pod identity association.
                    content:
                        application/json:
                            schema:
                                type: object
                                description: Object of IAM role arn.
                                properties:
                                  roleArn: 
                                    type: string
                                    description: The value of the IAM Role ARN for which the assume role policy has been updated.
                '400':
                    description: Bad request. One or more required fields are missing or invalid.
```


### Lambda関数の内容(29行目のprincipalArnを変更する)
```
import { EKSClient, DeleteAccessEntryCommand, ListAssociatedAccessPoliciesCommand, CreateAccessEntryCommand} from "@aws-sdk/client-eks";
import { IAMClient, UpdateAssumeRolePolicyCommand } from "@aws-sdk/client-iam";
const client = new EKSClient(process.config);
const iamClient = new IAMClient(process.config);
export const handler = async (event, context) => {
    console.log("Received event", event);
    console.log("Request Body values: ", event['requestBody']['content']['application/json']['properties']);
    // Extract the action group, api path, and parameters from the prediction
    var action = event["actionGroup"];
    var api_path = event["apiPath"];
    var httpMethod = event["httpMethod"];
    var response_body, response_code, body, command, res, reason;
    var clusterName, principalArn;
    var roleArn;
    if (api_path == '/createAccessEntry') {
        try {
            var array = event['requestBody']['content']['application/json']['properties'];
            array.forEach((element) => {
                if (element['name'] == 'clusterName')
                    clusterName = element['value'];
                else if (element['name'] == 'principalArn')
                    principalArn = element['value'];
            });
            // ************************************************* //
            // ************** Create Access Entry **************  //
            // ************************************************* //
            const input = { // CreateAccessEntryRequest
                clusterName: "jam-eks-cluster", // required
                principalArn: "arn:aws:iam::<account-id>:role/eks-pod-test-role", // required
              };
            const command = new CreateAccessEntryCommand(input);
            const response = await client.send(command);
            body = { accessEntryArn: "Fix the code to create access entry", accessPolicy: "No access policy attached" };
            response_code = 200;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
        catch (error) {
            if (error instanceof Error) {
                reason = error.message + "API Call - ${api_path}";
            }
            else
                reason = "error occurred in API call ${api_path}";
            body = { error: reason };
            response_code = 400;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
    }
    else if (api_path == '/describeAccessEntry') {
        try {
            var array = event['requestBody']['content']['application/json']['properties'];
            array.forEach((element) => {
                if (element['name'] == 'clusterName')
                    clusterName = element['value'];
                else if (element['name'] == 'principalArn')
                    principalArn = element['value'];
            });
            // Describe Access Entry's attached Access policies
            var input2 = {
                clusterName: clusterName,
                principalArn: principalArn
            };
            command = new ListAssociatedAccessPoliciesCommand(input2);
            res = await client.send(command);
            const ans = res['associatedAccessPolicies'];
            if (ans != undefined) {
                const newArray = ans.map(obj => {
                    const newObj = { ...obj };
                    delete newObj['associatedAt'];
                    delete newObj['modifiedAt'];
                    return newObj;
                });
                body = newArray;
                response_code = 200;
                response_body = { "application/json": { "body": JSON.stringify(body) } };
            }
        }
        catch (error) {
            if (error instanceof Error) {
                reason = error.message + "API Call - ${api_path}";
            }
            else
                reason = "error occurred in API call ${api_path}";
            body = { error: reason };
            response_code = 400;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
    }
    else if (api_path == '/deleteAccessEntry') {
        try {
            var array = event['requestBody']['content']['application/json']['properties'];
            array.forEach((element) => {
                if (element['name'] == 'clusterName')
                    clusterName = element['value'];
                else if (element['name'] == 'principalArn')
                    principalArn = element['value'];
            });
            // Delete Access Entry from the EKS Cluster
            var input3 = {
                clusterName: clusterName,
                principalArn: principalArn
            };
            command = new DeleteAccessEntryCommand(input3);
            res = await client.send(command);
            response_code = 200;
            response_body = { "application/json": { "body": "Successfully deleted the access entry" } };
        }
        catch (error) {
            if (error instanceof Error) {
                reason = error.message + "API Call - ${api_path}";
            }
            else
                reason = "error occurred in API call ${api_path}";
            body = { error: reason };
            response_code = 400;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
    }
    else if (api_path == '/updateRolePodIdentity') {
        try {
            // ********************************************************************* //
            // ************** Update IAM role's assume role policy ************** //
            // ********************************************************************* //
            var array = event['requestBody']['content']['application/json']['properties'];
            array.forEach((element) => {
                if (element['name'] == 'roleArn')
                    roleArn = element['value'];
            });
            const input = {
                PolicyDocument: `{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"pods.eks.amazonaws.com"},"Action":["sts:AssumeRole","sts:TagSession"]}]}`,
                RoleName: "eks-pod-test-role"
              };
            const command = new UpdateAssumeRolePolicyCommand(input);
            const response = await iamClient.send(command);
            body = { roleArn: "Fix the code to update the role" };
            response_code = 200;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
        catch (error) {
            if (error instanceof Error) {
                reason = error.message + "API Call - ${api_path}";
            }
            else
                reason = "error occurred in API call ${api_path}";
            body = { error: reason };
            response_code = 400;
            response_body = { "application/json": { "body": JSON.stringify(body) } };
        }
    }
    else {
        body = { error: "Incorrect API Path. Try another way" };
        response_code = 400;
        response_body = { "application/json": { "body": JSON.stringify(body) } };
    }
    var action_response = {
        'actionGroup': action,
        'apiPath': api_path,
        'httpMethod': httpMethod,
        'httpStatusCode': response_code,
        'responseBody': response_body
    };
    var session_attributes = event['sessionAttributes'];
    var prompt_session_attributes = event['promptSessionAttributes'];
    var api_response = {
        'messageVersion': '1.0',
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    };
    return api_response;
};

```
### プロンプト(task1)
```
Create an access entry for arn:aws:iam::<account-id>:role/eks-pod-test-role for the EKS cluster jam-eks-cluster.
```
### プロンプト(task2)
```
Remove the access entry for arn:aws:iam::<account-id>:role/eks-pod-test-role for the EKS cluster jam-eks-cluster.
```
### プロンプト(task3)
```
Modify the role arn:aws:iam::<account-id>:role/eks-pod-test-role to make it compatible with EKS Pod Identity Association.
```




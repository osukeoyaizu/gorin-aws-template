## task1
イベントバス(OrderEventBus)にルール作成

### Foodルール
名前:Food

イベントパターン:{ "detail": { "OrderType": ["Food"] } }

ターゲット:Lambda(FoodOrdersLambdaFunction)

### Beverageルール
名前:Beverage

イベントパターン:{ "detail": { "OrderType": ["Beverage"] } }

ターゲット:Lambda(BeverageOrdersLambdaFunc)


## task2
Lambda関数(OrdersLambdaFunction, FoodOrdersLambdaFunction, BeverageOrdersLambdaFunc)の環境変数を正しく設定する

## task3
Lambda関数(FoodOrdersLambdaFunction,BeverageOrdersLambdaFunc)に紐づくロールにdynamodb:PutItemの権限を付与する

APIGatewayからテストする

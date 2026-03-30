## task1
EC2インスタンス(I Love Cats Server)に紐づくロールのarnを回答する

## task2(勝手にクリアになる?)
EC2インスタンス(I Love Cats Server)に紐づくロールにインラインポリシー作成
```
{
    "Version": "2012-10-17",
    "Statement": [{
    	"Effect": "Deny",
    	"Action": "*",
        "Resource": "*",
    	"Condition": {
  	      "StringNotEquals": {
        	    "aws:ec2InstanceSourceVPC": "${aws:SourceVpc}"
    	    },
 	       "BoolIfExists": {
            	"aws:ViaAWSService": "false"
        	}
    	}
	}]
}
```

## task1
### main.tfの内容
```
data "aws_vpc" "selected_vpc" {
  tags = {
	  Name = "ChallengeVPC"
	}
}

data "aws_subnet" "selected_subnet" {
  tags = {
	  Name = "ChallengePublicSubnet1"
	}
}

resource "aws_security_group" "webserver_securitygroup" {
	vpc_id = data.aws_vpc.selected_vpc.id
  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "TCP"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazonlinuxami" {
	most_recent = true
	owners = ["amazon"]
	filter {
    name   = "architecture"
    values = ["x86_64"]
  }
	filter {
		name = "name"
		values = ["al2023-ami-*"]
  }
}

resource "aws_instance" "web-server" {
  ami           = data.aws_ami.amazonlinuxami.id
  instance_type = "c5.xlarge"
  subnet_id     = data.aws_subnet.selected_subnet.id
  vpc_security_group_ids = [aws_security_group.webserver_securitygroup.id]
  associate_public_ip_address = true
  user_data = <<-EOF
	  #!/bin/bash
	  sudo su
	  yum update -y
	  yum install -y httpd.x86_64
	  systemctl start httpd.service
	  systemctl enable httpd.service
	  echo "<h1>Hello TinkerLand World from $(hostname -f)</h1>" > /var/www/html/index.html
	EOF
	tags = {
		"Name" = "MyWebServer"
	} 
}
```


## task2
import.tfファイルを{WAF-ID}を既存のWAFのIDに変えてプッシュする
### import.tfの内容
```
import {
 # ID of the cloud resource
 #This needs to be replaced with your specific WACL's value!
 id = "{WAF-ID}/PublicStoreFrontALBWebACL/REGIONAL"
 
 # Resource address
 to = aws_wafv2_web_acl.PublicStoreFrontWebACL
}

resource "aws_wafv2_web_acl" "PublicStoreFrontWebACL" {
  # ...instance configuration...
  name = "PublicStoreFrontALBWebACL"
  scope = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "filter-requests-with-admin-parameter"
    priority = 0

    action {
      block {}
    }

    statement {
      byte_match_statement {

        positional_constraint = "CONTAINS"
        search_string = "yes"

        field_to_match { 
          single_query_argument {
            name = "admin"
          }
        }
        
        text_transformation {
            priority = 0
            type = "LOWERCASE"
        }

      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "filter-requests-with-admin-parameter"
      sampled_requests_enabled   = false
    }

  }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "PublicStoreFrontWebACLMetrics"
      sampled_requests_enabled   = false
    }

}
```

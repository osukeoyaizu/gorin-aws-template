
provider "aws" {
  region = "ap-northeast-1" # 東京リージョン例
}

# -------------------------
# VPC
# -------------------------
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name  = var.environment_name
    (var.tag_key) = var.tag_value
  }
}

# -------------------------
# Internet Gateway
# -------------------------
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name  = var.environment_name
    (var.tag_key) = var.tag_value
  }
}

# -------------------------
# Public Subnets
# -------------------------
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_1_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name  = "${var.environment_name}-sub-pub01-az1"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_2_cidr
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name  = "${var.environment_name}-sub-pub01-az2"
    (var.tag_key) = var.tag_value
  }
}

# -------------------------
# Private Subnets
# -------------------------
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_1_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name  = "${var.environment_name}-sub-prv01-az1"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_2_cidr
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name  = "${var.environment_name}-sub-prv01-az2"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_subnet" "private_3" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_3_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name  = "${var.environment_name}-sub-prv02-az1"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_subnet" "private_4" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_4_cidr
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name  = "${var.environment_name}-sub-prv02-az2"
    (var.tag_key) = var.tag_value
  }
}

# -------------------------
# NAT Gateways + EIPs
# -------------------------
resource "aws_eip" "nat_1" {
  domain = "vpc"
}

resource "aws_eip" "nat_2" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat_1" {
  allocation_id = aws_eip.nat_1.id
  subnet_id     = aws_subnet.public_1.id
}

resource "aws_nat_gateway" "nat_2" {
  allocation_id = aws_eip.nat_2.id
  subnet_id     = aws_subnet.public_2.id
}

# -------------------------
# Route Tables
# -------------------------
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name  = "${var.environment_name}-rtb-pub01"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public_1_assoc" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2_assoc" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

# Private Route Tables
resource "aws_route_table" "private_az1" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name  = "${var.environment_name}-rtb-prv01-az1"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_route" "private_az1_nat" {
  route_table_id         = aws_route_table.private_az1.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_1.id
}

resource "aws_route_table_association" "private_1_assoc" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_az1.id
}

resource "aws_route_table" "private_az2" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name  = "${var.environment_name}-rtb-prv01-az2"
    (var.tag_key) = var.tag_value
  }
}

resource "aws_route" "private_az2_nat" {
  route_table_id         = aws_route_table.private_az2.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_2.id
}

resource "aws_route_table_association" "private_2_assoc" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_az2.id
}

# -------------------------
# Data Sources
# -------------------------
data "aws_availability_zones" "available" {}

# -------------------------
# Variables
# -------------------------
variable "environment_name" {
  default = "vpc01"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_1_cidr" {
  default = "10.0.1.0/24"
}

variable "public_subnet_2_cidr" {
  default = "10.0.2.0/24"
}

variable "private_subnet_1_cidr" {
  default = "10.0.101.0/24"
}

variable "private_subnet_2_cidr" {
  default = "10.0.102.0/24"
}

variable "private_subnet_3_cidr" {
  default = "10.0.201.0/24"
}

variable "private_subnet_4_cidr" {
  default = "10.0.202.0/24"
}

variable "tag_key" {
  default = "Owner"
}

variable "tag_value" {
  default = "your-name-or-email"
}

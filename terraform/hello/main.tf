terraform {
  required_version = ">=1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>6.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "hello" {
  bucket = "uptime-sentinel-hello-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = "uptime-sentinel"
    Environment = "dev"
    Owner = "luca"
    ManagedBy = "terraform"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.hello.bucket
}

output "ARN"{
    value = aws_s3_bucket.hello.arn
}
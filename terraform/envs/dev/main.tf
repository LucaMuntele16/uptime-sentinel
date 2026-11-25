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

output "environment" {
  value = "dev"
}

locals {
  project = "uptime-sentinel"
  env     = "dev"

  tags = {
    Project     = local.project
    Environment = local.env
    ManagedBy   = "terraform"
  }
}

module "storage" {
  source     = "../../modules/storage"
  table_name = "${local.project}-${local.env}-results"
  tags       = local.tags
}

module "registry" {
  source          = "../../modules/registry"
  repository_name = "${local.project}-${local.env}-checker"
  tags            = local.tags
}

output "table_name" {
  value = module.storage.table_name
}

output "repository_url" {
  value = module.registry.repository_url
}
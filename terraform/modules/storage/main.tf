resource "aws_dynamodb_table" "results"{
    name = var.table_name
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "site"
    range_key = "timestamp"

    attribute {
      name = "site"
      type = "S"
    }

    attribute {
      name = "timestamp"
      type = "S"
    }

    ttl {
        attribute_name = var.ttl_attribute
        enabled = true
    }

    tags = var.tags
}
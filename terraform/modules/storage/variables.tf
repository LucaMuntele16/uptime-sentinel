variable "table_name"{
    type = string
    description = "DynamoDB table name"
}

variable "ttl_attribute"{
    type = string
    description = "Atribute for ttl"
    default = "ttl"
}

variable "tags"{
    type = map(string)
    default = {}
}
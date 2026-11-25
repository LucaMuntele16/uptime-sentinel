variable "repository_name" {
    type = string
    description = "ECR repo name"
}

variable "max_images" {
    type = number
    description = "number of images we keep"
    default = 10
}

variable "tags" {
    type = map(string)
    default = {}
}
resource "aws_ecr_repository" "this" {
    name = var.repository_name
    image_tag_mutability = "IMMUTABLE"

    image_scanning_configuration {
      scan_on_push = true
    }

    tags = var.tags
}

resource "aws_ecr_lifecycle_policy" "this" {
  repository = aws_ecr_repository.this.name

  policy = jsonencode({
    rules = [{
        rulePriority = 1
        description = "Store the last ${var.max_images} images"
        selection = {
            tagStatus = "any"
            countType = "imageCountMoreThan"
            countNumber = var.max_images
        }
        action = {
            type = "expire"
        }
    }]
  })
}
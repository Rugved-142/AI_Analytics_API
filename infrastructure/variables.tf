variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  default     = "ai-analytics"
}

variable "lambda_image_uri" {
  type        = string
  description = "ECR image URI for backend"
}

variable "domain_name" {
  type        = string
  default     = ""
}

variable "db_password_secret_arn" {
  type = string
}

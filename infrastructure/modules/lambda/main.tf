variable "project_name" { type = string }
variable "image_uri" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "lambda_security_group_id" { type = string }
variable "rds_endpoint" { type = string }
variable "redis_endpoint" { type = string }
variable "kafka_bootstrap" { type = string }
variable "domain_name" { type = string }
variable "db_password_secret_arn" { type = string }

resource "aws_ecr_repository" "this" {
  name = "${var.project_name}-backend"
}

resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "this" {
  function_name = "${var.project_name}-api"
  package_type  = "Image"
  image_uri     = var.image_uri
  role          = aws_iam_role.lambda.arn
  timeout       = 30
  memory_size   = 1024

  environment {
    variables = {
      DB_SECRET_ARN           = var.db_password_secret_arn
      DATABASE_HOST           = var.rds_endpoint
      REDIS_URL               = "redis://${var.redis_endpoint}:6379/0"
      KAFKA_BOOTSTRAP_SERVERS = var.kafka_bootstrap
    }
  }

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [var.lambda_security_group_id]
  }
}

resource "aws_apigatewayv2_api" "this" {
  name          = "${var.project_name}-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.this.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.this.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.this.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = "$default"
  auto_deploy = true
}

output "function_name" { value = aws_lambda_function.this.function_name }
output "api_endpoint" { value = aws_apigatewayv2_api.this.api_endpoint }
output "ecr_repository_url" { value = aws_ecr_repository.this.repository_url }

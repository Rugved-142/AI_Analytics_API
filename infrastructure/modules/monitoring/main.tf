variable "project_name" { type = string }
variable "lambda_name" { type = string }
variable "rds_identifier" { type = string }

resource "aws_cloudwatch_metric_alarm" "latency_p95" {
  alarm_name          = "${var.project_name}-latency-p95"
  namespace           = "AWS/ApiGateway"
  metric_name         = "Latency"
  statistic           = "p95"
  period              = 60
  evaluation_periods  = 1
  threshold           = 200
  comparison_operator = "GreaterThanThreshold"
}

resource "aws_cloudwatch_metric_alarm" "error_rate" {
  alarm_name          = "${var.project_name}-error-rate"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanThreshold"
  dimensions = {
    FunctionName = var.lambda_name
  }
}

resource "aws_cloudwatch_metric_alarm" "cold_start" {
  alarm_name          = "${var.project_name}-cold-starts"
  namespace           = "AWS/Lambda"
  metric_name         = "InitDuration"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 1000
  comparison_operator = "GreaterThanThreshold"
  dimensions = {
    FunctionName = var.lambda_name
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_connections" {
  alarm_name          = "${var.project_name}-rds-connections"
  namespace           = "AWS/RDS"
  metric_name         = "DatabaseConnections"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  dimensions = {
    DBInstanceIdentifier = var.rds_identifier
  }
}

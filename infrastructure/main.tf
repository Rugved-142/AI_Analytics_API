module "vpc" {
  source       = "./modules/vpc"
  project_name = var.project_name
}

module "rds" {
  source                 = "./modules/rds"
  project_name           = var.project_name
  vpc_id                 = module.vpc.vpc_id
  private_subnet_ids     = module.vpc.private_subnet_ids
  db_password_secret_arn = var.db_password_secret_arn
}

module "redis" {
  source             = "./modules/redis"
  project_name       = var.project_name
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
}

module "kafka" {
  source             = "./modules/kafka"
  project_name       = var.project_name
  private_subnet_ids = module.vpc.private_subnet_ids
  vpc_id             = module.vpc.vpc_id
}

module "lambda" {
  source             = "./modules/lambda"
  project_name       = var.project_name
  image_uri          = var.lambda_image_uri
  private_subnet_ids = module.vpc.private_subnet_ids
  lambda_security_group_id = module.vpc.lambda_security_group_id
  rds_endpoint       = module.rds.endpoint
  redis_endpoint     = module.redis.endpoint
  kafka_bootstrap    = module.kafka.bootstrap_brokers
  domain_name        = var.domain_name
  db_password_secret_arn = var.db_password_secret_arn
}

module "monitoring" {
  source        = "./modules/monitoring"
  project_name  = var.project_name
  lambda_name   = module.lambda.function_name
  rds_identifier = module.rds.identifier
}

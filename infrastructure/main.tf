terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "networking" {
  source       = "./modules/networking"
  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = "10.0.0.0/16"
}

module "ecr" {
  source       = "./modules/ecr"
  project_name = var.project_name
  environment  = var.environment
}

module "ecs" {
  source             = "./modules/ecs"
  project_name       = var.project_name
  environment        = var.environment
  aws_region         = var.aws_region
  db_secret_arn      = module.rds.db_secret_arn
  vpc_id             = module.networking.vpc_id
  backend_target_arn = module.alb.backend_target_arn
  alb_sg_id          = module.alb.alb_sg_id
  ecr_repo_url       = module.ecr.ecr_repo_url
  private_subnet_ids = module.networking.private_subnet_ids
  db_name = local.db_name
  db_endpoint = module.rds.db_endpoint
  redis_host_port = module.elasticache.redis_host_port
  redis_secret_arn = module.elasticache.redis_secret_arn
}

module "rds" {
  source             = "./modules/rds"
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  backend_sg_id      = module.ecs.backend_sg_id
  project_name       = var.project_name
  environment        = var.environment
  db_name            = local.db_name
}

module "elasticache" {
  source             = "./modules/elasticache"
  project_name       = var.project_name
  environment        = var.environment
  private_subnet_ids = module.networking.private_subnet_ids
  backend_sg_id      = module.ecs.backend_sg_id
  vpc_id             = module.networking.vpc_id
}

module "alb" {
  source            = "./modules/alb"
  project_name      = var.project_name
  vpc_id            = module.networking.vpc_id
  public_subnet_ids = module.networking.public_subnet_ids
  certificate_arn   = module.acm.certificate_arn
}

module "acm" {
  source = "./modules/acm"
}

module "vpc_endpoints" {
  source = "./modules/vpc_endpoints"
  vpc_id = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  private_route_table_id = module.networking.private_route_table_id
  backend_sg_id = module.ecs.backend_sg_id
  aws_region = var.aws_region
}

module "monitoring" {
  source = "./modules/monitoring"
  project_name = var.project_name
  aws_region = var.aws_region
  alert_email = var.alert_email
  alb_arn_suffix = module.alb.alb_arn_suffix
  backend_target_arn_suffix = module.alb.backend_target_arn_suffix
  ecs_service_name = module.ecs.ecs_service_name
  ecs_cluster_name = module.ecs.ecs_cluster_name
  db_id = module.rds.db_id
}

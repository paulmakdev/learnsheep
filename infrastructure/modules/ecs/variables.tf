variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "db_secret_arn" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "backend_target_arn" {
  type = string
}

variable "alb_sg_id" {
  type = string
}

variable "ecr_repo_url" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "db_name" {
  type = string
}

variable "db_endpoint" {
  type = string
}

variable "redis_host_port" {
  type = string
}

variable "redis_secret_arn" {
  type = string
}

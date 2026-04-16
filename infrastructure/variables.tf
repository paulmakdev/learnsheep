variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "learnsheep"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "alert_email" {
  description = "Email that will receive resource monitoring alerts"
  type = string
  default = "monitoring@learnsheep.com"
}

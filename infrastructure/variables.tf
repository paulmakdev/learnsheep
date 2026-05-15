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

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_domain_name_dev" {
  description = "Name of our domain"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_bucket_name_dev" {
  description = "Name of our S3 website bucket"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_sub_domain_dev" {
  description = "Sub domain for publishing"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_domain_name_prod" {
  description = "Name of our domain"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_bucket_name_prod" {
  description = "Name of our S3 website bucket"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "website_sub_domain_prod" {
  description = "Sub domain for publishing"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "github_org" {
  description = "Owner of repository holding the website"
  type = string
}

# Will be defined in dev or web.tfvars, usage: -var-file: {file_name}
variable "github_repo" {
  description = "Repository holding the website"
  type = string
}

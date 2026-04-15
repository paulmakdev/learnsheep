output "ecr_repo_url" {
  value = module.ecr.ecr_repo_url
}

output "cert_validation_options" {
  value = module.acm.cert_validation_options
}

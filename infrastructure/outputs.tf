output "ecr_repo_url" {
  value = module.ecr.ecr_repo_url
}

output "cert_validation_options" {
  value = module.acm.cert_validation_options
}

output "website_validation_options_dev" {
  value = module.website_dev.website_validation_options
}

output "website_validation_options_prod" {
  value = module.website_prod.website_validation_options
}

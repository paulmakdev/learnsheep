output "cert_validation_options" {
  value = aws_acm_certificate.api.domain_validation_options
}

output "certificate_arn" {
  value = aws_acm_certificate.api.arn
}

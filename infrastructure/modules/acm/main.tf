# This is going to generate the certificate and give us the cname records we need to add
resource "aws_acm_certificate" "api" {
  domain_name       = "api.learnsheep.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

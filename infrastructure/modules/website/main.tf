locals {
  hostname = var.sub_domain == "@" ? var.domain_name : "${var.sub_domain}.${var.domain_name}"
}

terraform {
  required_providers {
    cloudflare = {
      source = "cloudflare/cloudflare"
    }
  }
}

provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

data "cloudflare_zone" "main" {
  filter = {
    name = var.domain_name
  }
}

resource "aws_s3_bucket" "frontend" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_acm_certificate" "frontend" {
  provider = aws.virginia

  domain_name       = local.hostname
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "cloudflare_dns_record" "acm_validation" {
  for_each = {
    (local.hostname) = {
      name  = tolist(aws_acm_certificate.frontend.domain_validation_options)[0].resource_record_name
      value = tolist(aws_acm_certificate.frontend.domain_validation_options)[0].resource_record_value
      type  = tolist(aws_acm_certificate.frontend.domain_validation_options)[0].resource_record_type
    }
  }

  zone_id = data.cloudflare_zone.main.zone_id

  # strip trailing dot that ACM adds to record names
  name    = trimsuffix(each.value.name, ".")
  content = each.value.value
  type    = each.value.type

  ttl     = 60
  proxied = false
}

resource "aws_acm_certificate_validation" "frontend" {
  provider = aws.virginia

  certificate_arn = aws_acm_certificate.frontend.arn

  # FIX: use .hostname (full FQDN) not .name (short label)
  validation_record_fqdns = [
    for record in cloudflare_dns_record.acm_validation :
    record.name
  ]
}

resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${var.bucket_name}-oac"
  description                       = "OAC for frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  default_root_object = "index.html"

  aliases = [local.hostname]

  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "s3-origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-origin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.frontend.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  depends_on = [aws_acm_certificate_validation.frontend]
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontAccess"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.frontend.arn
          }
        }
      }
    ]
  })
}

resource "cloudflare_dns_record" "frontend" {
  zone_id = data.cloudflare_zone.main.zone_id
  name    = var.sub_domain
  type    = "CNAME"
  content = aws_cloudfront_distribution.frontend.domain_name
  proxied = true
  ttl     = 1
}


# IAM ROLES

locals {
  name_suffix = var.sub_domain == "@" ? "-prod" : "-${var.sub_domain}"
  role_name   = "${var.project_name}-website-role${local.name_suffix}"
  policy_name = "${var.project_name}-website-s3-cloudfront${local.name_suffix}"
}

resource "aws_iam_role" "frontend" {
  name = local.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "frontend" {
  name = local.policy_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.frontend.arn,
          "${aws_s3_bucket.frontend.arn}/*"
        ]
      },
      {
        Sid    = "CloudFrontAccess"
        Effect = "Allow"
        Action = [
          "cloudfront:CreateInvalidation",
          "cloudfront:GetInvalidation",
          "cloudfront:ListInvalidations"
        ]
        Resource = aws_cloudfront_distribution.frontend.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "frontend" {
  role       = aws_iam_role.frontend.name
  policy_arn = aws_iam_policy.frontend.arn
}

data "aws_caller_identity" "current" {}

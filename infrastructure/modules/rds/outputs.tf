output "db_secret_arn" {
  value     = aws_db_instance.postgres.master_user_secret[0].secret_arn
  sensitive = true
}

output "db_endpoint" {
    value = aws_db_instance.postgres.endpoint
}

output "db_id" {
  value = aws_db_instance.postgres.id
}

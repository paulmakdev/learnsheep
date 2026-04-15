output "redis_host_port" {
  value = "${aws_elasticache_replication_group.redis.primary_endpoint_address}:${aws_elasticache_replication_group.redis.port}"
}

output "redis_secret_arn" {
  value = aws_secretsmanager_secret.redis.arn
}

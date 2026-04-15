# Subnet group — ElastiCache must be in private subnets
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-redis-subnet-group"
  subnet_ids = var.private_subnet_ids
}

resource "random_password" "redis" {
  length  = 64
  special = false
}

resource "aws_secretsmanager_secret" "redis" {
  name = "${var.project_name}-auto-redis-secret"
}

resource "aws_secretsmanager_secret_version" "redis" {
  secret_id     = aws_secretsmanager_secret.redis.id
  secret_string = jsonencode({
    secret_key = random_password.redis.result
  })
}

# Security group — only accept connections from ECS backend
resource "aws_security_group" "redis_sg" {
  name   = "${var.project_name}-redis-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.backend_sg_id]
  }
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id           = "${var.project_name}-redis"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_clusters      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis_sg.id]

  # Maintenance during low-traffic window
  maintenance_window = "sun:05:00-sun:06:00"

  # Optional but recommended for consistency/production safety (don't need right now)
  automatic_failover_enabled = false

  auth_token = random_password.redis.result

  # Required by some compliance policies
  transit_encryption_enabled = true

  description = "Redis Cache for Learnsheep."

  tags = { Name = "${var.project_name}-redis" }
}

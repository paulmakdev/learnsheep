data "aws_secretsmanager_secret" "jwt_secret" {
  name = "${var.project_name}-jwt-secret"
}

# Execution role — ECS uses this to pull image + write logs
resource "aws_iam_role" "ecs_execution" {
  name = "${var.project_name}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role — backend uses this to call AWS services at runtime
resource "aws_iam_role" "ecs_task" {
  name = "${var.project_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "secrets-access"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = [
        "arn:aws:secretsmanager:${var.aws_region}:*:secret:${var.project_name}-*",
        "arn:aws:secretsmanager:${var.aws_region}:*:secret:rds!*"
      ]
    }]
  })
}

# Allow task to read from Secrets Manager
resource "aws_iam_role_policy" "ecs_task_secrets" {
  name = "secrets-access"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = ["arn:aws:secretsmanager:${var.aws_region}:*:secret:${var.project_name}-*"]
    }]
  })
}

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/${var.project_name}-backend"
  retention_in_days = 30
}

resource "aws_ecs_task_definition" "backend" {
  family                   = "${var.project_name}-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256" # 0.25 vCPU
  memory                   = "512" # 0.5 GB
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name      = "backend"
    image     = "${var.ecr_repo_url}:latest"
    essential = true

    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]

    # Non secret environment variables
    environment = [
      { name = "ENVIRONMENT", value = "production" },
      { name = "DB_ENDPOINT", value = var.db_endpoint },
      { name = "DB_NAME", value = var.db_name },
      { name = "REDIS_HOST_PORT", value = var.redis_host_port }
    ]

    # Secrets (from AWS)
    secrets = [
      {
        name = "JWT_SECRET",
        valueFrom = data.aws_secretsmanager_secret.jwt_secret.arn
      },
      {
        name = "DB_SECRET",
        valueFrom = var.db_secret_arn
      },
      {
        name = "REDIS_SECRET",
        valueFrom = var.redis_secret_arn
      }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.project_name}-backend"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "backend" {
  name            = "${var.project_name}-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  # our backend should be on the private subnet
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.backend_sg.id]
    assign_public_ip = false
  }

  # Allows ECS to deploy new task before killing old one
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [task_definition] # CI/CD manages this
  }

  load_balancer {
    target_group_arn = var.backend_target_arn
    container_name   = "backend"
    container_port   = 8000
  }
}

# This is the security group for the backend
resource "aws_security_group" "backend_sg" {
  name        = "backend_sg"
  description = "Allow traffic from ALB to FastAPI"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow API communication from ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [var.alb_sg_id] # only ALB can access
  }

  # We don't need any other communications, other than internally and the ALB. This only allows internal communication anywhere if necessary.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # ECR, Secrets Manager, CloudWatch, external APIs
  }

  tags = {
    Name = "backend_sg"
  }
}

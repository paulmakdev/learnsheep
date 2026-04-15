# DB Subnet Group — RDS must span 2 AZs
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.private_subnet_ids
  tags       = { Name = "${var.project_name}-db-subnet-group" }
}

resource "aws_db_instance" "postgres" {
  identifier        = "${var.project_name}-postgres"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro" # This is the smallest db we can do. Upgrade as needed, but should be fine for a while.
  allocated_storage = 20
  storage_type      = "gp2"

  db_name = var.db_name
  username = "postgres"

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  # Backups — 7 day retention, taken during likely low-traffic window
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"

  # Prevent accidental deletion
  deletion_protection = false # Set to true in real production when done
  skip_final_snapshot = true  # Set to false in real production when done

  # Performance insights — free tier available
  performance_insights_enabled = true

  # This makes AWS store the user password combo
  manage_master_user_password = true

  tags = { Name = "${var.project_name}-postgres" }
}

output "endpoint" {
  value     = aws_db_instance.postgres.endpoint
  sensitive = true
}

# This is the security group for the rds database
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow traffic from FastAPI to DB"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow API communication from FastAPI backend"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.backend_sg_id] # only backend can access
  }

  # We don't need any other communications, other than internally and the backend, so egress blocked

  tags = {
    Name = "rds_sg"
  }
}

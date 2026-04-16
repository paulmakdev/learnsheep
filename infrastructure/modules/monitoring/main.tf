# SNS Topic (email alerts)

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# ECS — Checks if no running tasks happened every minute (if it's at 0, we have a service outage!)

resource "aws_cloudwatch_metric_alarm" "ecs_task_count" {
  alarm_name          = "${var.project_name}-ecs-no-tasks"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "RunningTaskCount"
  namespace           = "ECS/ContainerInsights"
  period              = 60
  statistic           = "Minimum"
  threshold           = 1

  alarm_description = "CRITICAL: No ECS tasks running; backend is down"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = var.ecs_service_name
  }
}

# ALB — 5XX errors (backend/server failures) -> set to threshold 5 per 5 minutes x 2 must happen before alert
# This one will likely need to change in the future depending on traffic / stability

resource "aws_cloudwatch_metric_alarm" "alb_5xx" {
  alarm_name          = "${var.project_name}-alb-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 300
  statistic           = "Sum"
  threshold           = 5

  alarm_description = "ALB target 5XX errors detected — backend failing"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = var.alb_arn_suffix
    TargetGroup  = var.backend_target_arn_suffix
  }
}

# ALB — unhealthy targets, is the target unhealthy at least once in 2 1 minute periods?

resource "aws_cloudwatch_metric_alarm" "alb_unhealthy_targets" {
  alarm_name          = "${var.project_name}-alb-unhealthy-targets"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "UnHealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Average"
  threshold           = 0

  alarm_description = "ALB has unhealthy targets — check backend"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = var.alb_arn_suffix
    TargetGroup  = var.backend_target_arn_suffix
  }
}

# ALB — latency (slow backend). This is important because we are currently operating minimally, need to know when to upgrade

resource "aws_cloudwatch_metric_alarm" "alb_latency" {
  alarm_name          = "${var.project_name}-alb-high-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "TargetResponseTime"
  namespace           = "AWS/ApplicationELB"
  period              = 300
  statistic           = "Average"
  threshold           = 1.5

  alarm_description = "ALB latency too high — backend slow"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = var.alb_arn_suffix
    TargetGroup  = var.backend_target_arn_suffix
  }
}

# ECS CPU utilization

resource "aws_cloudwatch_metric_alarm" "ecs_cpu" {
  alarm_name          = "${var.project_name}-ecs-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  alarm_description = "ECS CPU above 80% — consider scaling"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = var.ecs_service_name
  }
}

# ECS memory utilization -- we REALLY don't want memory failures

resource "aws_cloudwatch_metric_alarm" "ecs_memory" {
  alarm_name          = "${var.project_name}-ecs-high-memory"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 85

  alarm_description = "ECS memory usage high — risk of OOM kills or instability"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName  = var.ecs_service_name
  }
}

# RDS — low storage, self explanatory

resource "aws_cloudwatch_metric_alarm" "rds_storage" {
  alarm_name          = "${var.project_name}-rds-low-storage"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 2000000000  # 2GB

  alarm_description = "RDS storage low — expand soon"
  alarm_actions     = [aws_sns_topic.alerts.arn]

  dimensions = {
    DBInstanceIdentifier = var.db_id
  }
}


# Cloudwatch dashboard

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project_name}-overview"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          region = var.aws_region
          title  = "ALB Requests & 5XX Errors"
          period = 300
          stat   = "Sum"
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", var.alb_arn_suffix],
            [".", "HTTPCode_Target_5XX_Count", ".", ".", { "yAxis": "right" }]
          ]
        }
      },
      {
        type = "metric"
        properties = {
          region = var.aws_region
          title  = "ALB Healthy vs Unhealthy Targets"
          period = 60
          stat   = "Average"
          metrics = [
            ["AWS/ApplicationELB", "HealthyHostCount", "LoadBalancer", var.alb_arn_suffix, "TargetGroup", var.backend_target_arn_suffix],
            [".", "UnHealthyHostCount", ".", ".", ".", ".", { "yAxis": "right" }]
          ]
        }
      },
      {
        type = "metric"
        properties = {
          region = var.aws_region
          title  = "ECS CPU & Memory"
          period = 300
          stat   = "Average"
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ClusterName", var.ecs_cluster_name, "ServiceName", var.ecs_service_name],
            [".", "MemoryUtilization", ".", ".", ".", ".", { "yAxis": "right" }]
          ]
        }
      },
      {
        type = "metric"
        properties = {
          region = var.aws_region
          title  = "ECS Running Task Count"
          period = 60
          stat   = "Average"
          metrics = [
            ["ECS/ContainerInsights", "RunningTaskCount", "ClusterName", var.ecs_cluster_name, "ServiceName", var.ecs_service_name]
          ]
        }
      },
      {
        type = "metric"
        properties = {
          region = var.aws_region
          title  = "RDS Free Storage"
          period = 300
          stat   = "Average"
          metrics = [
            ["AWS/RDS", "FreeStorageSpace", "DBInstanceIdentifier", var.db_id]
          ]
        }
      }
    ]
  })
}

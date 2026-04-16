output "backend_target_arn" {
  value = aws_lb_target_group.backend_target.arn
}

output "alb_sg_id" {
  value = aws_security_group.alb_sg.id
}

output "alb_dns_name" {
  value = aws_lb.backend_alb.dns_name
}

output "backend_target_arn_suffix" {
  value = aws_lb_target_group.backend_target.arn_suffix
}

output "alb_arn_suffix" {
  value = aws_lb.backend_alb.arn_suffix
}

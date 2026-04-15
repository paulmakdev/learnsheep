variable "private_subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
    type = string
}

variable "private_route_table_id" {
    type = string
}

variable "backend_sg_id" {
    type = string
}

variable "aws_region" {
    type = string
}

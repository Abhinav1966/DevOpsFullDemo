variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "app_name" {
  type    = string
  default = "devops-ml-app"
}
variable "container_port" {
  type    = number
  default = 5000
}

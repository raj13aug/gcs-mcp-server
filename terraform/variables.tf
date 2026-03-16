variable "project_id" {
  default = "vm-group-448915"
}

variable "region" {
  default = "us-central1"
}

variable "cloudrun_name" {
  default = "cloudrun-service"
}
variable "cloudrun_ingress" {
  default = "INGRESS_TRAFFIC_ALL"
}

variable "cloudrun_image" {
  default = "raj13aug/my-app:1.0"
}
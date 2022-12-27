variable "region" {
  type    = string
  default = "us-east-1"
}

variable "project" {
  type = string
}

variable "alarm_email_topic" {
  type = string
}

variable "subscription_emails" {
  type = list(string)
}

variable "created_by" {
  type = string
}

variable "event_rule_name" {
  type = string
}

variable "log_group_name" {
  type = string
}

variable "lambda_function_name" {
  type = string
}

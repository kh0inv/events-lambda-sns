provider "aws" {
  region = var.region
}

resource "aws_sns_topic" "alarm_email_topic" {
  name = var.alarm_email_topic
  tags = {
    "createdby" = var.created_by
  }
}

resource "aws_sns_topic_subscription" "alarm_email_subscription" {
  topic_arn = aws_sns_topic.alarm_email_topic.arn
  count     = length(var.subscription_emails)
  protocol  = "email"
  endpoint  = var.subscription_emails[count.index]
}

resource "aws_cloudwatch_event_rule" "alarm_email_rule" {
  name           = var.event_rule_name
  description    = "Capture CloudWatch alarm state change. Routes to log group and lamda function"
  event_bus_name = "default"
  is_enabled     = true

  event_pattern = jsonencode({
    source      = ["aws.cloudwatch"]
    detail-type = ["CloudWatch Alarm State Change"]
    detail = {
      state = {
        value = ["ALARM"]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "log_group_target" {
  rule      = aws_cloudwatch_event_rule.alarm_email_rule.name
  target_id = "SendTo-${var.log_group_name}"
  arn       = aws_cloudwatch_log_group.alarm_group.arn
}

resource "aws_cloudwatch_event_target" "lambda_function_target" {
  rule      = aws_cloudwatch_event_rule.alarm_email_rule.name
  target_id = "SendTo-${var.lambda_function_name}"
  arn       = aws_lambda_function.change_email_function.arn
}

resource "aws_cloudwatch_log_group" "alarm_group" {
  name = "/aws/events/${var.log_group_name}"

  tags = {
    "createdby" = var.created_by
  }
}

resource "null_resource" "zip_code" {
  provisioner "local-exec" {
    command = "tar -cvzf changeAlarmEmail.zip changeAlarmEmail.py"
  }
}

resource "aws_lambda_function" "change_email_function" {
  function_name = var.lambda_function_name
  description   = "Create message to send email"
  runtime       = "python3.9"
  role          = aws_iam_role.email_function_role.arn
  handler       = "changeAlarmEmail.lambda_handler"

  filename         = "changeAlarmEmail.zip"
  source_code_hash = filebase64sha256("changeAlarmEmail.zip")

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.alarm_email_topic.arn
      PROJECT_NAME  = var.project
    }
  }

  depends_on = [
    null_resource.zip_code
  ]

  tags = {
    "createdby" = var.created_by
  }
}

resource "aws_lambda_permission" "permission_for_events_to_invoke_lambda" {
  statement_id  = "${var.project}-AllowExecutionFromEvents"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.change_email_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.alarm_email_rule.arn
}

resource "aws_iam_role" "email_function_role" {
  name = "${var.project}-email-function-role"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "sts:AssumeRole",
        Principal = {
          Service = ["lambda.amazonaws.com"]
        }
      }
    ]
  })

  inline_policy {
    name = "${var.project}-email-function-policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow",
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          Resource = "arn:aws:logs:*:*:log-group:/aws/lambda/*"
        },
        {
          Effect = "Allow",
          Action = [
            "sns:Publish"
          ],
          Resource = aws_sns_topic.alarm_email_topic.arn
        }
      ]
    })
  }

  tags = {
    "createdby" = var.created_by
  }
}

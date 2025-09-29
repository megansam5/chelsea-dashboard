provider "aws" {
  region     = var.REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}

# =========================== DATA ===========================
data "aws_vpc" "chelsea_vpc" {
  id = var.VPC_ID
}

data "aws_subnet" "chelsea_public_subnet1" {
  id = var.SUBNET_ID1
}

data "aws_ecr_image" "daily_extraction_image" {
  repository_name = var.DAILY_EXTRACTION_ECR_REPO
  image_tag       = "latest"
}

data "aws_s3_bucket" "chelsea_s3_bucket" {
  bucket = var.S3_BUCKET_NAME
}

# =========================== Lambda Extraction Pipeline ===========================

resource "aws_iam_role" "lambda_execution_role" {
  name = "chelsea-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_s3_access" {
  name = "chelsea-lambda-s3-access"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          data.aws_s3_bucket.chelsea_s3_bucket.arn,
          "${data.aws_s3_bucket.chelsea_s3_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "daily_extraction_log_group" {
  name              = "/aws/lambda/chelsea-daily-extraction"
  retention_in_days = 7
}

resource "aws_lambda_function" "daily_extraction_lambda" {
  function_name = "chelsea-daily-extraction"
  image_uri     = data.aws_ecr_image.daily_extraction_image.image_uri
  role          = aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"
  timeout       = 900
  memory_size   = 512

  environment {
    variables = {
      S3_BUCKET_NAME = var.S3_BUCKET_NAME
      REGION         = var.REGION
      DB_HOST        = var.DB_HOST
      DB_PORT        = var.DB_PORT
      DB_USER        = var.DB_USER
      DB_PASSWORD    = var.DB_PASSWORD
      DB_NAME        = var.DB_NAME
    }
  }

  image_config {
    command = ["pipeline.lambda_handler"]
  }

  depends_on = [
    aws_cloudwatch_log_group.daily_extraction_log_group,
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]
}

# =========================== EventBridge Scheduler ===========================

resource "aws_iam_role" "eventbridge_scheduler_role" {
  name = "chelsea-eventbridge-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "scheduler.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_invoke_lambda" {
  name = "chelsea-eventbridge-invoke-lambda"
  role = aws_iam_role.eventbridge_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = aws_lambda_function.daily_extraction_lambda.arn
      }
    ]
  })
}

resource "aws_scheduler_schedule" "daily_extraction_schedule" {
  name = "chelsea-daily-extraction-schedule"

  # Run daily at midnight UTC
  schedule_expression          = "cron(0 0 * * ? *)"
  schedule_expression_timezone = "UTC"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.daily_extraction_lambda.arn
    role_arn = aws_iam_role.eventbridge_scheduler_role.arn

    input = jsonencode({
      source = "eventbridge.scheduler"
    })
  }
}

# =========================== EC2 Dashboard ===========================

resource "tls_private_key" "ec2_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key_file" {
  content         = tls_private_key.ec2_key.private_key_pem
  filename        = "${path.module}/chelsea-key-pair.pem"
  file_permission = "0400"
}

resource "aws_key_pair" "ec2_key_pair" {
  key_name   = "chelsea-key-pair"
  public_key = tls_private_key.ec2_key.public_key_openssh
}

resource "aws_security_group" "dashboard_sg" {
  name        = "chelsea-dashboard-sg"
  description = "Security group for Chelsea dashboard EC2"
  vpc_id      = data.aws_vpc.chelsea_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "chelsea-dashboard-sg"
  }
}

resource "aws_iam_role" "ec2_role" {
  name = "chelsea-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "ec2_s3_access" {
  name = "chelsea-ec2-s3-access"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          data.aws_s3_bucket.chelsea_s3_bucket.arn,
          "${data.aws_s3_bucket.chelsea_s3_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "chelsea-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "dashboard_ec2" {
  ami                         = "ami-0c0493bbac867d427"
  instance_type               = "t3.micro"
  key_name                    = aws_key_pair.ec2_key_pair.key_name
  subnet_id                   = data.aws_subnet.chelsea_public_subnet1.id
  vpc_security_group_ids      = [aws_security_group.dashboard_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3 python3-pip git
              EOF

  tags = {
    Name = "chelsea-dashboard"
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "local_file" "ec2_connection_info" {
  content = <<-EOF
    EC2_HOST=${aws_instance.dashboard_ec2.public_dns}
    EC2_IP=${aws_instance.dashboard_ec2.public_ip}
    SSH_COMMAND=ssh -i ${path.module}/chelsea-key-pair.pem ec2-user@${aws_instance.dashboard_ec2.public_ip}
  EOF

  filename = "${path.module}/ec2.env"
}

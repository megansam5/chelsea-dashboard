variable "REGION" {
    type = string 
    default = "eu-west-2"
}

variable "VPC_ID" {type = string}
variable "SUBNET_ID1" {type = string}


variable "ECS_CLUSTER_NAME" {type = string}

variable "AWS_ACCESS_KEY" {type = string}
variable "AWS_SECRET_KEY" {type = string}

variable "DAILY_EXTRACTION_ECR_REPO" {type = string}


variable "S3_BUCKET_NAME" {type = string}

variable "DB_HOST" {type = string}
variable "DB_PORT" {type = string}
variable "DB_PASSWORD" {type = string}
variable "DB_USER" {type = string}
variable "DB_NAME" {type = string}

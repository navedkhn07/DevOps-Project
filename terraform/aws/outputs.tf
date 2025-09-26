output "vpc_id" {
  value       = aws_vpc.main.id
  description = "ID of the created VPC"
}

output "public_subnet_ids" {
  value       = [for s in aws_subnet.public : s.id]
  description = "Public subnet IDs"
}

output "instance_public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web instance"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.app.bucket
  description = "S3 bucket name"
}


